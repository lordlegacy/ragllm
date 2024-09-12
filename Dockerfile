# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Set the FLASK_APP environment variable to point to the app
ENV FLASK_APP=langchain/app.py

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
