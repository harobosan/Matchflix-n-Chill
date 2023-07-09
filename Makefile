all:
	flask --app project run

static:
	pylint project

clean:
	rm -r ./instance/ ./project/__pycache__/

test:
	pytest tests/. -v

coverage:
	pytest tests/. -v --cov=project

install: requirements.txt
	pip install -r requirements.txt

