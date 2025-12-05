FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port (Railway provides PORT dynamically)
EXPOSE ${PORT:-8080}

# Start command with dynamic PORT
CMD gunicorn app:app --bind 0.0.0.0:${PORT:-8080}
