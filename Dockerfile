# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (same as your Flask app's port)
EXPOSE 5000

# Define environment variable (Optional)
ENV FLASK_ENV=production

# Command to run the app
CMD ["python", "app.py"]
