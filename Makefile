install:
	poetry install

test:
	python manage.py test

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --force-reinstall dist/*.whl

lint:
	flake8 order_flow orders

selfcheck:
	poetry check

check: test

dev:
	python manage.py runserver 0.0.0.0:8000

PORT ?= 8000

.PHONY: install

shell:
	python manage.py shell_plus --ipython

test-coverage:
	poetry run coverage run manage.py test -v 2 && poetry run coverage xml

load:
	python manage.py loaddata orders.json
	python manage.py loaddata products.json
	python manage.py loaddata order_details.json

migrate:
	python manage.py migrate

start: migrate load test dev