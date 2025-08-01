# Use an older base image with known vulnerabilities for this demo
FROM python:3.8-slim-buster

WORKDIR /app
# Install dependencies first to leverage Docker layer caching.
# We install flask directly here as it's the only dependency for the app.
# The requirements.txt in the root is for the CI script, not this app.
RUN pip install --no-cache-dir flask==1.1.2
 
# Copy the application file into the container.
COPY app.py .
 
CMD ["python", "app.py"]
