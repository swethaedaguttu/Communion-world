# Use Python 3.10-slim as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /events

# Copy the local code to the container
COPY . /events

# Install dependencies (if you have a requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Expose a port if needed (optional)
EXPOSE 5000

# Define the command to run your application
CMD ["python", "events.py"]
