# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt (if any)
RUN pip install -r requirements.txt

# output is buffered by default in non-interactive environments.
ENV PYTHONUNBUFFERED=1

# Expose the port the app runs on
EXPOSE 8081

# Run the server when the container launches
CMD ["python", "webserver.py"]
