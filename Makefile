TAG := kolibri-indexer

build-docker:
	docker build -t $(TAG) .

bash:
	docker run --rm -it --network=host -v $$(PWD):/shared --workdir /shared $(TAG) bash

db:
	docker run \
             -e POSTGRES_HOST_AUTH_METHOD=trust \
             -v $$(pwd)/pg_data:/var/lib/postgresql/data \
             -p 5432:5432 \
             postgres -c log_statement=all
