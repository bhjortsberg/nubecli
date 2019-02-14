
env: requirements.txt
	virtualenv -p python3 env
	./env/bin/pip3 install --upgrade pip
	./env/bin/pip install --requirement requirements.txt

clean:
	rm -rf ./env
