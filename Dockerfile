# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that your app runs on
EXPOSE 8080

# Specify the command to run the application
CMD ["gunicorn", "-k", "gevent", "-b", "0.0.0.0:8080", "app:app"]  # Change 'app:app' if your main file or app instance is named differently