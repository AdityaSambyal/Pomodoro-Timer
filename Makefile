# Makefile helpers
.PHONY: build-pyinstaller

build-pyinstaller:
	./scripts/build_mac_pyinstaller.sh ".venv/bin/python"
