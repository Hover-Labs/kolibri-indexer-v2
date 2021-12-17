TAG := kolibri-indexer

build-docker:
	docker build -t $(TAG) .

bash:
	docker run --rm -it  -v $$(PWD):/shared --workdir /shared $(TAG) bash
