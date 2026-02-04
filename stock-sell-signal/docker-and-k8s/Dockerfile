FROM python:3.12-slim

WORKDIR /app

# Install Dependencies listed in requirements.txt
COPY docker-and-k8s/requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# Copy inference.py and model artifact i,e model_v1.pkl
COPY ../fast-api-app.py .
COPY ../model_v1.pkl .

EXPOSE 8000

# Run inference script
CMD ["uvicorn", "fast-api-app:app", "--host", "0.0.0.0", "--port", "8000"]

