FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY init_db.py .
COPY data/ ./data/
COPY templates/ ./templates/

# Initialize users.json if it doesn't exist
RUN python init_db.py

# Expose port 5000 (but will bind to 127.0.0.1 only)
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]

