all:
	flask --app project run

static:
	pylint project

clean:
	rm -r ./instance/ ./project/__pycache__/

install: requirements.txt
	pip install -r requirements.txt

