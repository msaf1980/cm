init:
	pip install -r requirements.txt

test:
	nosetests tests

doc:
	$(MAKE) -C docs html latexpdf

.PHONY: docs
