# Photo Auto Tag Processor (Docker + Synology)

## 📖 Project Overview
Photo Auto Tag Processor is a tool for automated photo tagging, metadata enrichment, and organization. It uses Azure Vision API for image analysis and ExifTool for metadata management. Designed for easy deployment with Docker, including on Synology NAS.

**GitHub repository:** [https://github.com/ChrisPolewiak/photo-indexer](https://github.com/ChrisPolewiak/photo-indexer)

## 🗂️ Project Structure

- `index.py` — Main processing script.
- `utils/` — Utility modules (EXIF, Azure, logging, file handling, etc.).
- `.env.example` — Example environment configuration.
- `.camera_owners-example.json` — Example camera ownership metadata.
- `docker-compose.yml` — Docker Compose configuration.
- `Dockerfile` — Docker build instructions.
- `start-container.sh` / `update-and-restart.sh` — Helper scripts for running/updating the container.
- `requirements.txt` — Python dependencies.

## ⚙️ Configuration Files

### `.env`
Main environment variables for Docker and the application.  
Example:
```
VISION_ENDPOINT="https://your-api-name.cognitiveservices.azure.com"
VISION_KEY="your-vision-api-key"
IMPORT_PATH=/volume1/photo-import
LIBRARY_PATH=/volume1/photo-library
LIBRARYTEST_PATH=/volume1/photo-library-test
SOURCE_DIR=/data/import
TARGET_DIR=/data/library
TARGET_TEST_DIR=/data/library_test
SYSLOG_IP="SYSLOG_IP"
LINUX_UID="UID"
LINUX_GID="GID"
```
- `VISION_ENDPOINT`, `VISION_KEY`: Azure Vision API credentials.
- `IMPORT_PATH`, `LIBRARY_PATH`, `LIBRARYTEST_PATH`: Host paths for import/library/test folders.
- `SOURCE_DIR`, `TARGET_DIR`, `TARGET_TEST_DIR`: Container paths for import/library/test folders.
- `SYSLOG_IP`: (Optional) Syslog server IP for logging.
- `LINUX_UID`, `LINUX_GID`: User/group IDs for file permissions (should match your Synology user).

### `.camera_owners.json`
Maps camera make/model to author/copyright/label metadata.
Example:
```json
{
  "Apple iPhone 15 Pro": {
    "author": "Name Surname",
    "copyright": "url or something else",
    "label": "LabelName"
  },
  "Unknown": {
    "author": "",
    "copyright": "",
    "label": ""
  }
}
```

## 🚀 Quick Start

```bash
git clone https://github.com/ChrisPolewiak/photo-indexer.git
cd photo-indexer
cp .env.example .env
nano .env  # Fill in your configuration
docker compose up --build
```

## 🏠 Deploying on Synology NAS

1. **Install Docker** via Synology Package Center.
2. **Clone the repository** to a shared folder (e.g., `/volume1/docker/photo-indexer`):
   ```sh
   git clone https://github.com/ChrisPolewiak/photo-indexer.git /volume1/docker/photo-indexer
   ```
3. **Prepare configuration**:
   - Copy `.env.example` to `.env` and edit paths/keys.
   - Copy `.camera_owners-example.json` to `.camera_owners.json` and customize.
4. **Map volumes** in `.env` to your Synology photo folders.
5. **Build and run**:
   ```sh
   cd /volume1/docker/photo-indexer
   docker compose up --build
   ```
6. **(Optional)** Use `start-container.sh` or `update-and-restart.sh` for automated management (e.g., via scheduled tasks).

## 📝 Usage Notes

- The container reads from `IMPORT_PATH` and writes to `LIBRARY_PATH` (and test path if in test mode).
- Azure Vision API credentials are required for image analysis.
- Metadata is written using ExifTool; ensure your Synology user has permissions for the mapped folders.
- Logs are sent to syslog if configured.

## 🛠️ Troubleshooting

- Check Docker logs for errors:  
  `docker logs photo-indexer`
- Ensure `.env` and `.camera_owners.json` are present and correctly configured.
- For permission issues, verify `LINUX_UID` and `LINUX_GID` match your Synology user.

## 📚 Further Documentation

- See comments in each utility module in [`utils/`](utils/) for details on specific functionality.
- For Azure Vision API setup, refer to [Azure documentation](https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/).
- For the latest updates and issues, visit the [GitHub repository](https://github.com/ChrisPolewiak/photo-indexer).


