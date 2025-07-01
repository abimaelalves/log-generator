FROM python:3.11-slim
WORKDIR /app
COPY log_emitter.py .
CMD ["python", "log_emitter.py"]
