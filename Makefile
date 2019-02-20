
env: requirements.txt
	virtualenv -p python3 env
	./env/bin/pip3 install --upgrade pip
	./env/bin/pip3 install --requirement requirements.txt

install: env
	./env/bin/python3 setup.py install
	ln -sf $(PWD)/env/bin/ccli $(HOME)/bin/

clean:
	rm -rf ./env
	rm -f $(HOME)/bin/ccli
