build-docker-image:
	docker build -t local-chat --no-cache tools

run-docker-container:
	docker run -itP local-chat
