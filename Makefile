venv:
	virtualenv venv; \
	source venv/bin/activate; \

install:
	pip install -r requirements.txt; \

clean:
	deactivate; \
    rm -rf venv; \
    find -iname "*.pyc" -delete; \