FROM python:3.12-slim

WORKDIR /app

# Copy project configuration
COPY pyproject.toml ./

# Copy all code (shared + this service)
COPY code/ ./code/

# Install dependencies
RUN pip install --no-cache-dir -e .

# Expose port
EXPOSE 8000

# Run the API service
CMD ["uvicorn", "services.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
