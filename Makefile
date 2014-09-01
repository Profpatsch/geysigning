PROGRAM = geysigning
VENV_NAME = $(PROGRAM)
FILES = geysign.sh *.py

test:
	pylint $(FILES)
	pep8 $(FILES)

dev_environment:
	pip install -r requirements.txt

clean:
		rm -f *.pyc
