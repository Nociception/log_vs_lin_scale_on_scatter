.PHONY: run create-virtualenv help install

run:
	printf "A matplotlib window is going to pop:\n\
	it is recommended to resize it full screen.\n"
	python3 src/main.py

create-virtualenv:
	python3 -m virtualenv env
	@printf "\nRun on your own this command in your terminal:\n\
	source env/bin/activate\n"

install:
	pip install -r requirements.txt

help:
	@printf "Here are the Makefile's rules available:\n\
	run:\n\
		Runs this simple command: python3 src/main.py\n\
		As it is the first rule, \"make\" is enough to reach it.\n\
		Remind that this program has some dependencies,\n\
		which you must install before any run.\n\
		Installing them in a virtual environment is recommended.\n\
	create-virtualenv:\n\
		To avoid any packages version conflicts,\n\
		installing the required dependencies in a virtual environment\n\
		is an usual simple three-steps procedure\n\
		(the second requires you to type a specific command\n\
		in your terminal):\n\
		1. run \"make create-virtualenv\"\n\
			Runs \"python3 -m virtualenv env\"\n\
		2. type \"source env/bin/activate\" in your terminal.\n\
	install:\n\
		3. run \"make install\"\n\
			Runs \"pip install -r requirements.txt\"\n\
			It will install all the dependencies the program needs.\n"
