# Start from base image
FROM python:3.11-slim

# Set initial working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Change working directory to your Django project folder
WORKDIR /app/credit

# Set environment variable so Python can find your modules
ENV PYTHONPATH=/app

# Run Gunicorn from inside /app/credit
CMD ["gunicorn", "credit.wsgi:application", "--bind", "0.0.0.0:8000"]