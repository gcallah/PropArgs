
prod: tests github

github:
	- git commit -a
	git push origin master

tests:
	pytest

package: tests
	rm -rf dist/*
	$(PY_EXEC) setup.py sdist bdist_wheel
	$(PY_EXEC) -m twine upload dist/*

