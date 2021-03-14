
prod: tests github

github:
	git commit -a
	git push origin master

tests:
	pytest

package: tests
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*

