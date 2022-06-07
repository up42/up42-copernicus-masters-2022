### Dockerfile to build the UP42 block.

# Use a standard python image as a base
FROM up42/up42-blockutils-py37
ARG BUILD_DIR=.

# The manifest file contains metadata for correctly building and
# tagging the Docker image. This is a build time argument.
ARG manifest

# Include the variables in the website
ARG user
ARG password

LABEL "up42_manifest"=$manifest

# ASF user & password
ENV USER $user
ENV PASSWORD $password

# Working directory setup.
WORKDIR /block
COPY $BUILD_DIR/requirements.txt /block

# Install the Python requirements.
RUN pip3 install -r requirements.txt

# Copy the code into the container.
COPY $BUILD_DIR/src /block/src

# Invoke run.py.
CMD ["python", "/block/src/data_block.py"]
