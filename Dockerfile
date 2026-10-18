FROM python:3.14-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY organs/ ./organs/
COPY synapses/ ./synapses/
COPY contract.json .
COPY kernel.py .

CMD ["python", "kernel.py"]
