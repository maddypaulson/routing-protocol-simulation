# Define the docker image name
IMAGE_NAME=routing-simulation

# Default action is to show help
all: help

# Help command to show available options
help:
	@echo "Available commands:"
	@echo "  build-image      - Build the Docker image for the routing simulation"
	@echo "  run-lsr          - Run the link state routing simulation"
	@echo "  run-dvr          - Run the distance vector routing simulation"
	@echo "  clean            - Remove output files and Docker containers"
	@echo "  clean-docker     - Remove Docker image"

# Build the Docker image
build-image:
	docker build -t $(IMAGE_NAME) .

# Run the link state routing simulation
run-lsr:
	docker run -it --rm -v "$$(pwd)":/app $(IMAGE_NAME) python src/linkstate.py topology.txt message.txt change.txt

# Run the distance vector routing simulation
run-dvr:
	docker run -it --rm -v "$$(pwd)":/app $(IMAGE_NAME) python src/distancevector.py topology.txt message.txt change.txt

# Clean output files
clean:
	rm -f output.txt

# Clean up Docker image
clean-docker:
	docker rmi $(IMAGE_NAME)