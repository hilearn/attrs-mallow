PROJECT = marshenum
PYTHON_VERSION=3.7
venv_name = py${PYTHON_VERSION}-${PROJECT}
venv = .venv/${venv_name}

# Commands that activate and run virtual environment versions.
_python = . ${venv}/bin/activate; python
_pip = . ${venv}/bin/activate; pip

default: update_venv
.PHONY: default

${venv}: PYTHON_PREFIX=
${venv}/bin/pip: requirements.txt
	${PYTHON_PREFIX}python${PYTHON_VERSION} -m venv ${venv}
	${_pip} install --upgrade pip --cache .tmp/
	${_pip} install -r requirements.txt --cache .tmp/


update_venv: requirements.txt ${venv}
	${_pip} install -r requirements.txt --cache .tmp/
	@ln -fs ${venv_name} .venv/current
	@echo Success, to activate the development environment, run:
	@echo "\tsource .venv/current/bin/activate"
.PHONY: update_venv

publish:
	${_python} setup.py sdist bdist_wheel
	twine upload dist/*
.PHONY: publish

test:
	python -m pytest tests
.PHONY: test
