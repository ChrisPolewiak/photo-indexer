# Photo Auto Tag Processor (Docker + Synology)

## 🔧 Wymagania
- Docker + Docker Compose
- Python 3.12 (w kontenerze)
- Zewnętrzny `.env` plik z kluczami i ścieżkami

## 🚀 Szybki start

```bash
git clone git@github.com:your-user/photo-auto.git
cd photo-auto
cp .env.example .env
nano .env  # uzupełnij dane
docker compose up --build
