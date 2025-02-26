.PHONY: run create-virtualenv help install


run:
	printf "A matplotlib window is going to pop:\n\
	it is recommended to resize it full screen.\n"
	python3 src/main.py


create-virtualenv:
	sudo apt install virtualenv

	@if [ -f ./env/bin/activate ]; then \
		printf "Virtual environment already set.\n\
		Skipping creation...\n\
		activate it (with make source env/bin/activate),\n\
		and install dependencies (with make install) if you have not done it yet,\n\
		or deactivate it (with deactivate).\n"; \
	else \
		printf "Virtual environment creation...\n"; \
		python3 -m virtualenv env; \
		printf "\nVirtual environment created.\n\
		Run on your own this command in your terminal:\n\
		\n\tsource env/bin/activate\n\n\
		Remind to deactivate it once you are done with this project usage session\n\
		(whether your delete or not the cloned repo on your computer): deactivate\n"; \
	fi


install:
	printf "If you encounter errors or packages versions conflicts\n\
	with your local installed packages, consider using a virtual environment\n\
	(make create-virtualenv)\n"
	pip install -r requirements.txt
	sudo apt-get install python3-tk


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
