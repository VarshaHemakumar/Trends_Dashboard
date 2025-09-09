# Use lightweight Python base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 8080

# Run Gunicorn (Flask app)
CMD ["gunicorn", "-b", ":8080", "app:app"]
