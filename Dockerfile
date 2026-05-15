FROM python:3.12-slim

WORKDIR /my_app

# Install dependencies first to leverage Docker cache.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and model/data files.
COPY . .

EXPOSE 8000

CMD ["uv", "run", "litestar", "--app", "main:app", "run", "--host", "0.0.0.0", "--port", "8000"]
