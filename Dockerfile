# Base tray: an official, small Linux image that already contains Python 3.14
FROM python:3.14-slim

# Every next instruction works inside /app (created if it does not exist)
WORKDIR /app

# First only the ingredients list, then install the ingredients
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then the code of the application
COPY app/ ./app/

# Documentation: the app listens on port 8000
EXPOSE 8000

# The command that runs each time a container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
