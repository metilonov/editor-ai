FROM python:3.12-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        ca-certificates \
        libglib2.0-0 \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

RUN python -m pip install --upgrade pip setuptools wheel

RUN python -m pip uninstall -y \
    opencv-python \
    opencv-python-headless \
    opencv-contrib-python \
    opencv-contrib-python-headless \
    || true

RUN python -m pip install --no-cache-dir -r /app/requirements.txt

RUN python -c "assert hasattr(__import__('cv2'),'CascadeClassifier')"

COPY . /app

RUN mkdir -p /app/data /app/temp /app/output /app/logs

CMD ["python", "run.py"]
