# Use a slim Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Ensure the app has permissions to write the .db file
RUN chmod 666 /app

# Run the pipeline
CMD ["python", "-m", "src.main"]