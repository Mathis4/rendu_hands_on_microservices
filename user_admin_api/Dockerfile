# Use a lightweight Python image
FROM python:3.11-slim

# Install FastAPI and Uvicorn
RUN pip install fastapi uvicorn asyncpg requests_unixsocket
# Copy the application code
COPY user_admin_api.py /app/user_admin_api.py
# Set the working directory to /app
WORKDIR /app
# Expose UDS path as a volume
VOLUME ["/tmp"]
# Run Uvicorn using the Unix Domain Socket
CMD ["uvicorn", "user_admin_api:app", "--uds", "/tmp/api_socket.sock"]
