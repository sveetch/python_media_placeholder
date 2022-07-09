"""
Build an unique GIF animation from options.

Animation is very basic but should includes enough random content to be guaranteed as
unique, thanks to uuid and random colors.

Original code comes from https://note.nkmk.me/en/python-pillow-gif/
"""
import datetime
import hashlib
import json
import uuid
import random

from pathlib import Path

import click
import humanize

from PIL import Image
from PIL import ImageDraw


# A set of configurations for expected (not exactly) file size
SIZE_CONFIGS = {
    "58KiB": {
        "width": 200,
        "colors": ["black", "white"],
        "radius": 1.5,
        "step": 8,
        "duration": 40,
    },
    "596KiB": {
        "width": 400,
        "colors": ["black", "white"],
        "radius": 6.5,
        "step": 2,
        "duration": 40,
    },
    "1.1MiB": {
        "width": 600,
        "colors": ["black", "white"],
        "radius": 20,
        "step": 2,
        "duration": 10,
    },
    "144KiB": {
        "width": 200,
        "colors": ["black", "white", "grey", "cyan", "gold"],
        "radius": 1.5,
        "step": 8,
        "duration": 40,
    },
    "3MiB": {
        "width": 600,
        "colors": ["black", "white", "grey", "cyan", "gold"],
        "radius": 20,
        "step": 2,
        "duration": 10,
    },
    "4MiB": {
        "width": 600,
        "colors": ["black", "white", "grey", "cyan", "gold", "beige", "aliceblue"],
        "radius": 1.5,
        "step": 2,
        "duration": 10,
    },
    # This may take from a minute to more, depending your system ressources (not so
    # much CPU is used but used memory may grow around 5Go more)
    "12MiB": {
        "width": 800,
        "colors": ["black", "white", "grey", "cyan", "gold", "beige", "aliceblue"],
        "radius": 8.5,
        "step": 1,
        "duration": 10,
    },
}


class BuilderGif:
    def __init__(self):
        pass

    def write_text(self, drawer, width, text_color):
        """
        Write text into given image.

        Arguments:
            drawer (object): PIL drawer interface for an image.
            width (integer): Image width.
            text_color (string): Color name to draw text.
        """
        # Unique text build from uuid
        text_content = str(uuid.uuid4())

        # Dummy text write position
        drawer.text(
            (
                (width - drawer.textlength(text_content)) / 2,
                20
            ),
            text_content,
            fill=text_color,
        )

    def animate_circle(self, images, width, max_radius, step, center, square_color,
                       circle_color, text_color="red"):
        """
        Make circle animation in a square.
        """
        a = 1
        for i in range(0, max_radius, step):
            #print("   {})".format(a), i)
            im = Image.new(
                "RGB",
                (width, width),
                square_color,
            )
            draw = ImageDraw.Draw(im)
            draw.ellipse(
                (center - i, center - i, center + i, center + i),
                fill=circle_color,
            )
            self.write_text(draw, width, text_color)
            images.append(im)
            a += 1
        print("🎨 Drawed: {} frames (from 0 to {} max radius)".format(a-1, i))

    def create(self, destination, **kwargs):
        """
        Create an animated GIF image object.

        This will be a square with circle starting from center and going out of square
        twice. The first time with a color and the second with another, each part alternate
        square color and circle color.

        Arguments:
            destination (string or pathlib.Path): File destination path.

        Keywords Arguments:
            width (integer): Square width size in pixels.
            colors (list): List of color names to alternate.
            color_1 (tuple or string): First image background color and second circle color.
            color_2 (tuple or string): First circle color and second image background color.
            color_text (tuple or string): Text color for all series.
            radius (integer or float): Radius defines how far the circle radius is going.
                This is what determines the animation length to fill with frame step
            step (integer): Step between each frame, the more step there is, the less
                frames there will be to fill animation length (from radius).
            duration (integer): Duration in millisecond between frames. This does not impact
                file size, only the visual animation speed.

        NOTE:
            * Both Radius and Step determine the number of frames;
            * Number frames impact file size but no so much on its own;
            * Bigger radius will take circle to go farest out from the square layer, there
              will be more time with not much animation (since the circle will paint out
              of the layer);
            * Step have no size impact, it just make more detailled animation, which
              is not really visible with implemented animation;
            * For the same length of colors, different color names won't really impact
              file size;
        """
        # Every image frames register
        images = []

        # Set every required options from given kwargs and defaults
        width = kwargs.get("width", 200)
        colors = kwargs.get("colors", ["black", "white"])
        color_1 = kwargs.get("color_1", "black")
        color_2 = kwargs.get("color_2", "white")
        color_text = kwargs.get("color_text", "red")
        radius = kwargs.get("radius", 1.5)
        step = kwargs.get("step", 8)
        duration = kwargs.get("duration", 40)

        # Absolute center point position for given size
        center = width // 2
        # Max radius to go, this computes how far to go from the center point
        max_radius = int(center * 1.5)

        assert len(colors) >= 2

        # Rebuild a dict of options to fully dump them even if they are not passed as kwargs
        options = {
            "width": width,
            "colors": colors,
            "color_1": color_1,
            "color_2": color_2,
            "color_text": color_text,
            "radius": radius,
            "step": step,
            "duration": duration,
            "center": center,
            "max_radius": max_radius,
        }
        print("🔧 Config:", json.dumps(options, indent=4))

        for i, color_1 in enumerate(colors):
            not_current_color = [c for c in colors if(c != color_1)]
            color_2 = random.choice(not_current_color)
            self.animate_circle(
                images,
                width,
                max_radius,
                step,
                center,
                color_1,
                color_2,
                color_text
            )

        # Create final animation image from first image object filled with all other
        # image objects (they are added as next frames in order)
        images[0].save(
            destination,
            save_all=True,
            append_images=images[1:],
            optimize=False,
            duration=duration,
            loop=0,
        )

        return destination

    def batch(self, basedir, configs):
        """
        Run a batch creation of image files.
        """
        created_checksum = []
        now = datetime.datetime.now().isoformat(timespec="seconds").replace(":", "-")

        destination_path = basedir / now
        destination_path.mkdir(mode=0o777, parents=True)

        print()
        print("Running batch creation in:", destination_path)
        print()

        batch_key = uuid.uuid4()
        filename_pattern = "{batch_key}_{item_key}.gif"

        for item_key, config in enumerate(configs, start=1):
            start = datetime.datetime.now()

            filename = filename_pattern.format(
                batch_key=batch_key,
                item_key=item_key,
            )
            item_destination = destination_path / filename

            print()
            print("🚀 Create:", item_destination.name)
            self.create(item_destination, **config)

            # Compute elapsed time during creation
            end = datetime.datetime.now()
            duration = str(end - start)

            # Make some additional report
            file_checksum = hashlib.md5(open(item_destination, "rb").read()).hexdigest()
            file_size = humanize.naturalsize(
                item_destination.stat().st_size,
                binary=True
            )
            print("📈 Checksum:", file_checksum)
            print("📈 File size:", file_size)
            print("⏰ Elapsed:", duration)

            # Assert there is not twice checksum
            assert (file_checksum not in created_checksum) is True
            created_checksum.append(file_checksum)

        return destination_path


@click.command()
@click.option("--list", "list_mode", is_flag=True, help="List available configurations.")
@click.option("--total", default=1, help="Number of GIF file to create, default to 1.")
@click.option(
    "--config",
    default="58KiB",
    type=click.Choice(SIZE_CONFIGS.keys()),
    help=(
        "Configuration name to use for GIF builder. Default to '58KiB'. "
        "Use the '--list' option to display available configurations."
    ),
)
@click.option(
    "--destination",
    type=click.Path(
        file_okay=False, dir_okay=True, writable=True, resolve_path=True,
        path_type=Path,
    ),
    help=(
        "Directory path where to create new directory for created GIF files. Path can "
        "absolute or relative (to current directory). Default will create into "
        "'var/gifs/' directory relative to current directory."
    ),
)
def cli_interface(list_mode, total, config, destination):
    """
    Create GIF file from options.

    Any GIF will look almost the same but with some variance to make them unique.

    Default mode is to create GIF files but there is also a mode to list available
    GIF builder configurations.
    """
    if list_mode:
        click.echo("🗃️ Available configurations 🗃️")
        click.echo("")

        for name, options in SIZE_CONFIGS.items():
            click.echo("🔧 {}".format(name))

            if "width" in options:
                click.echo("   - Width: {}".format(options["width"]))
            if "colors" in options:
                click.echo("   - Colors: {}".format(options["colors"]))
            if "radius" in options:
                click.echo("   - Radius: {}".format(options["radius"]))
            if "step" in options:
                click.echo("   - Step: {}".format(options["step"]))
            if "duration" in options:
                click.echo("   - Duration: {}".format(options["duration"]))

            click.echo("")

    else:
        if not destination:
            destination = Path("./var").resolve() / "gifs"

        click.echo("Destination: {}".format(destination))
        click.echo("Configuration: {}".format(config))
        click.echo("Total to create: {}".format(total))

        builder = BuilderGif()

        # Will build "length" time of the same config
        configs = [SIZE_CONFIGS[config]] * total

        builder.batch(destination, configs)

        click.echo("")
        click.echo("🎉 Finished 🎉")


if __name__ == "__main__":
    cli_interface()
