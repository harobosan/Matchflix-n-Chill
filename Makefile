all:
	flask --app project run

static:
	pylint project

clean:
	rm -rf ./instance/
	find -name "__pycache__" -exec rm -rf {} \;

test:
	pytest tests/. -v

coverage:
	pytest tests/. -v --cov=project

install: requirements.txt
	pip install -r requirements.txt

