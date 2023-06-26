all:
	flask --app project run

#test:
#

clean:
	rm -r ./instance/ ./project/__pycache__/

install: requirements.txt
	pip install -r requirements.txt
