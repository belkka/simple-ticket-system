.PHONY: lint
lint: lint.txt

.PHONY: clean
clean:
	rm -f lint.txt


SOURCES := $(shell find ./app -name '*.py')
lint.txt: $(SOURCES)
	poetry run pycodestyle ./app | tee lint.txt
