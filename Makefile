.PHONY: venv system-packages python-packages install unit-tests integration-tests tests all

venv:
	pip3 install --user virtualenv
	virtualenv venv

system-packages:
	sudo apt install python-pip -y

python-packages:
	pip3 install -r requirements.txt

install: system-packages python-packages

unit-tests:
	python3 -m unittest -vvv \
		tests.unit.test_utils

integration-tests:
	python3 -m unittest -vvv \
		tests.integration.test_describe \
		tests.integration.test_profile \
		tests.integration.test_select \
		tests.integration.test_summary \
		tests.integration.test_events

tests: unit-tests integration-tests

all: install tests
