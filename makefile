
prod: tests github

github:
	- git commit -a
	git push origin master

tests:
	pytest

package: tests
	python setup.py sdist bdist_wheel
	python -m twine upload dist/*

