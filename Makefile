install:
	poetry install

test:
	poetry run python manage.py test

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --force-reinstall dist/*.whl

lint:
	poetry run flake8 order_flow orders

selfcheck:
	poetry check

check: selfcheck lint test

dev:
	poetry run python manage.py runserver

PORT ?= 8000

.PHONY: install

shell:
	python manage.py shell_plus --ipython

test-coverage:
	poetry run coverage run manage.py test -v 2 && poetry run coverage xml
