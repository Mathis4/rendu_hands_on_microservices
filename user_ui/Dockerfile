FROM python:3.11-slim

RUN pip install gradio requests requests_unixsocket

COPY user_ui.py /app/user_ui.py
WORKDIR /app

CMD ["python", "user_ui.py"]