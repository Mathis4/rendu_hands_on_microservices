FROM python:3.11-slim

RUN pip install gradio requests requests_unixsocket

COPY admin_ui.py /app/admin_ui.py
WORKDIR /app

CMD ["python", "admin_ui.py"]
