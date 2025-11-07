FROM python:3.12-slim-bookworm AS base

WORKDIR /usr/src/app

# Copy and install dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app code and static folder
COPY . .

# Set environment variable for port (optional)
ENV APP_PORT 8080

# Run the Flask app
ENTRYPOINT ["python", "app.py"]
