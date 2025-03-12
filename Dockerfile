FROM python:3.11

WORKDIR /app

# Copy requirements and install
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# Copy entire project (including scripts)
COPY . .

WORKDIR /app/backend

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]