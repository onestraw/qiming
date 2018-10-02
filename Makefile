PYTHON=venv/bin/python

tree:
	tree -I venv -P '*.py'

run:
	${PYTHON} qm.py

venv:
	virtualenv venv

deps:
	brew install opencc
	pip install -r requirements.txt

clean:
	find . -name '*.pyc' | xargs rm
