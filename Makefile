install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -p no:warnings  -vv testing.py

format:
	black *.py


lint:
	pylint --disable=R,C main.py  mlib.py

all: install lint
