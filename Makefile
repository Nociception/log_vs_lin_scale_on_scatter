.PHONY: run create-virtual-env install

run:
	python3 src/poo.py

create-virtual-env:
	python3 -m venv env
	@echo "Run on your own this command in your terminal:"
	@echo "source env/bin/activate"

install:
	pip install -r requirements.txt

