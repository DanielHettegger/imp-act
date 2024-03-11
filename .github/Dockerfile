# Use an official Python runtime as a parent image
FROM python:3.9-slim-bullseye

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install poetry
RUN pip install poetry

# Install project dependencies
RUN poetry install

# Set the default command to run when starting a container to bash shell
CMD ["bash"]