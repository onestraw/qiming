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

check:
	flake8 --ignore=E501,F401,E128,E402,E731,F821 crawler tools view qm.py

clean:
	find . -name '*.pyc' -exec rm {} \;
