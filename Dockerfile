FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    exiftool \
    libimage-exiftool-perl \
    libjpeg-dev \
    libheif-dev \
    build-essential \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*    

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONIOENCODING=utf-8

CMD ["python", "main.py"]
