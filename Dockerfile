FROM python:3.11-slim

# Instalujemy exiftool i inne wymagane pakiety
RUN apt-get update && \
    apt-get install -y exiftool libimage-exiftool-perl git && \
    apt-get clean

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj zależności i zainstaluj
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Skopiuj resztę kodu
COPY . .

# Uruchomienie domyślne (możesz zmienić na arg z entrypoint)
CMD ["python", "index.py"]
