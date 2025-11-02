FROM python:3.10.6

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Set the environment variable for the volume
ENV MOUNT_PATH=/app/volume

# Create the volume directory
RUN mkdir -p $MOUNT_PATH

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application with Gunicorn
CMD ["gunicorn", "--bind", ":8000", "--timeout", "180", "app:app"]
