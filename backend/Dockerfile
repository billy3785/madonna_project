# Use Python base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy dependencies file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files into the container
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
