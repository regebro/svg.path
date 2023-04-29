root_dir := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
ifdef NO_VENV
bin_dir :=
python_exe := python3
endif
ifndef NO_VENV
bin_dir := $(root_dir)/ve/bin/
python_exe := $(bin_dir)python3
endif

all: devenv check test

# The fullrelease script is a part of zest.releaser, which is the last
# package installed, so if it exists, the devenv is installed.
devenv:	$(bin_dir)fullrelease setup.cfg

$(bin_dir):
	virtualenv ve --python python3.9

$(bin_dir)fullrelease: $(bin_dir)
	$(python_exe) -m pip install -e .[test]

check: devenv
	$(bin_dir)black src tests
	$(bin_dir)flake8 src tests
	$(bin_dir)pyroma -d .
	$(bin_dir)check-manifest

coverage: devenv
	$(bin_dir)coverage run $(bin_dir)pytest
	$(bin_dir)coverage html
	$(bin_dir)coverage report

test: devenv
	$(bin_dir)pytest

release:
	$(bin_dir)fullrelease

clean:
	rm -rf ve .coverage htmlcov build .pytest_cache
