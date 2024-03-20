# Define variables for convenience
IMAGE_NAME=pa2_env

# The default make target. This will be triggered when you just run `make`.
all: adjust_dockerfile build_image compile_scripts

# Detects the system architecture and adjusts the Dockerfile accordingly
adjust_dockerfile:
	@ARCH=$(shell uname -m); \
	if [ "$$ARCH" = "x86_64" ]; then \
		echo "Detected x86_64 architecture"; \
		sed 's/FROM python:3.8-slim/FROM python:3.8-slim/' Dockerfile.template > Dockerfile; \
	elif [[ "$$ARCH" = "aarch64" || "$$ARCH" = "arm64" ]]; then \
		echo "Detected ARM architecture"; \
		sed 's|FROM python:3.8-slim|FROM arm64v8/python:3.8-slim|' Dockerfile.template > Dockerfile; \
	else \
		echo "Unknown architecture $$ARCH, using default"; \
	fi

# Builds the Docker image
build_image:
	docker build -t $(IMAGE_NAME) .

# Compiles the scripts into binaries using PyInstaller and ensures they are placed in the /obj folder
compile_scripts:
	docker run --rm -v "$(PWD)/dist:/app/dist" $(IMAGE_NAME) pyinstaller --onefile dvr.py
	docker run --rm -v "$(PWD)/dist:/app/dist" $(IMAGE_NAME) pyinstaller --onefile lsr.py


# Cleanup: Remove the image after compiling the binaries
clean:
	docker rmi $(IMAGE_NAME)

.PHONY: all adjust_dockerfile build_image compile_scripts clean
