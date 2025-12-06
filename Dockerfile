FROM python:3.11-slim

# Build version: 2025-12-06-v2 - Force rebuild
ARG CACHEBUST=1
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files - bust cache to get latest code
RUN echo "Cache bust: ${CACHEBUST}"
COPY . .

# Expose port (Railway provides PORT dynamically)
EXPOSE ${PORT:-8080}

# Start command with dynamic PORT
CMD gunicorn app:app --bind 0.0.0.0:${PORT:-8080}
