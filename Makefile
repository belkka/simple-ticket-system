SOURCES := $(shell find ./app -name '*.py')
lint.txt: $(SOURCES)
	poetry run pycodestyle ./app | tee lint.txt


.PHONY: clean
clean:
	rm -f lint.txt


.PHONY: fresh_run
fresh_run:
	docker-compose down
	docker-compose up -d
	sleep 5
	poetry run flask db_create_all
	poetry run flask run --debug
