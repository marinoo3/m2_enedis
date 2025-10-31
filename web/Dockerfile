FROM python:3.10.6
RUN mkdir -p /tmp && chmod -R 1777 /tmp

# Set environment to non-interactive
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source files
COPY . .

# Expose the port gunicorn will run on
EXPOSE 8000

# Run gunicorn when the container launches
CMD ["gunicorn", "--bind", ":8000", "--timeout", "180", "app:app"]
