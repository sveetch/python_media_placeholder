PYTHON_INTERPRETER=python3
VENV_PATH=.venv
PIP=$(VENV_PATH)/bin/pip
OPTIMUS=$(VENV_PATH)/bin/optimus-cli
PROJECT_DIR=project
SETTINGS_BASE=settings.base
SETTINGS_PROD=settings.production
SERVER_HOST="0.0.0.0:8001"


help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  install-backend     -- to install this Optimus project with virtualenv and Pip"
	@echo "  install             -- to install both backend and frontend"
	@echo
	@echo "  clean-pycache       -- to remove all __pycache__, this is recursive from current directory"
	@echo "  clean-builds        -- to remove everything builded"
	@echo "  clean-backend       -- to clean backend installation"
	@echo "  clean               -- to clean local repository from all stuff created during development"
	@echo

clean-pycache:
	@echo ""
	@echo "==== Clear Python cache ===="
	@echo ""
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*\.pyc"|xargs rm -f
.PHONY: clean-pycache

clean-builds:
	@echo ""
	@echo "==== Clear builds ===="
	@echo ""
	rm -Rf var
.PHONY: clean-builds

clean-backend:
	@echo ""
	@echo "==== Clear backend install ===="
	@echo ""
	rm -Rf $(VENV_PATH)
.PHONY: clean-backend

clean: clean-backend clean-builds clean-pycache
.PHONY: clean

venv:
	@echo ""
	@echo "==== Install virtual environment ===="
	@echo ""
	virtualenv -p $(PYTHON_INTERPRETER) $(VENV_PATH)
.PHONY: venv

install-backend: venv
	@echo ""
	@echo "==== Install backend ===="
	@echo ""
	$(PIP) install -r requirements.txt
.PHONY: install-backend

install: install-backend
.PHONY: install
