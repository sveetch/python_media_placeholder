"""
Convert MP4 to MP4

Convert previously created unique MP4 from ``gif.py`` is a quick and effortless way to
produce MP4 videos than to build them from scratch.
"""
import hashlib
import datetime

from pathlib import Path

import click
import humanize

import ffmpy

VAR_PATH = Path("./var").resolve() / "mp4s"


class GifToMp4Converter:
    def get_output_destination(self, source_filepath, destination_filepath):
        """
        Get the filename, replace suffix with ".mp4" and locate it in given destination
        directory.
        """
        return destination_filepath / (source_filepath.stem + ".mp4")

    def batch(self, source_path, destination_path):
        """
        Get the filename, replace suffix with ".mp4" and locate it in given destination
        directory.
        """
        if not destination_path.exists():
            destination_path.mkdir(mode=0o777, parents=True)

        for source_filepath in source_path.iterdir():
            destination_filepath = self.get_output_destination(
                source_filepath,
                destination_path,
            )

            if destination_filepath.exists():
                click.echo(
                    click.style(
                        "💥 Aborted, file already exists: {}".format(destination_filepath),
                        fg="yellow"
                    )
                )
                continue

            click.echo("")
            click.echo(
                click.style("🚀 Start converting 🚀", fg="green")
            )
            click.echo("- Source: {}".format(source_filepath))
            click.echo("- Destination: {}".format(destination_filepath))
            click.echo("")
            ff = ffmpy.FFmpeg(
                inputs={source_filepath: None},
                outputs={destination_filepath: None}
            )
            ff.run()
            click.echo("")

        return


@click.command()
@click.argument(
    "source",
    type=click.Path(
        file_okay=False, dir_okay=True, writable=True, resolve_path=True,
        path_type=Path, exists=True,
    ),
)
@click.option(
    "--destination",
    type=click.Path(
        file_okay=False, dir_okay=True, writable=True, resolve_path=True,
        path_type=Path,
    ),
    help=(
        "Directory path where to create new directory for created MP4 files. Path can "
        "absolute or relative (to current directory). Default will create into "
        "'var/mp4s/' directory relative to current directory."
    ),
)
def cli_interface(source, destination):
    """
    Convert GIF to basic MP4 files using FFMPEG.

    'SOURCE' argument is the required directory path where to get GIF files to convert.
    It won't be walked recursively.
    """
    if not destination:
        destination = Path("./var").resolve() / "mp4s"

    click.echo("Source: {}".format(source))
    click.echo("Destination: {}".format(destination))

    converter = GifToMp4Converter()

    converter.batch(source, destination)

    click.echo("")
    click.echo("🎉 Finished 🎉")


if __name__ == "__main__":
    cli_interface()
