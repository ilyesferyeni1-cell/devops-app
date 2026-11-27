# ---- Stage 1: the kitchen (builder) ----
FROM python:3.14-slim AS builder

WORKDIR /app

# Install the packages into one separate folder, easy to carry away
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- Stage 2: the plate (final image) ----
FROM python:3.14-slim
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/* && pip install --no-cache-dir --upgrade pip "setuptools>=78.1.1" urllib3 msgpack && pip uninstall -y setuptools

WORKDIR /app

# Take only the installed packages from the kitchen
COPY --from=builder /install /usr/local

# Then the code of the application
COPY app/ ./app/

# Documentation: the app listens on port 8000
EXPOSE 8000

# The command that runs each time a container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
