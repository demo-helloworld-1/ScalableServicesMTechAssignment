# Step 1: Use an official Python runtime as a parent image
FROM python:3.9-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the current directory contents into the container at /app
COPY . /app

# Step 4: Install any required packages
RUN pip install --no-cache-dir flask flask-cors requests

# Step 5: Make port 5002 available to the world outside this container
EXPOSE 5002

# Step 6: Define environment variable
ENV FLASK_ENV=development

# Step 7: Run the task service
CMD ["python", "task_service.py"]
