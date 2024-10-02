# Use the official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /Test

# Copy the current directory contents into the container at /app
COPY . /Test

# Run the application
CMD ["python", "Test.py"]
