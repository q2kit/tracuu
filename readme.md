# Tracuu Application

## Docker Setup

### Build the Docker image
```bash
docker build -t tracuu .
```

### Run the Docker container
```bash
docker run -p 8000:80 --name tracuu \
  -v /srv/tracuu/db.sqlite3:/srv/db.sqlite3 \
  -v /srv/tracuu/media:/srv/media \
  tracuu
```

### Volume Mounts
- **Database**: `/srv/tracuu/db.sqlite3` → `/srv/db.sqlite3`
- **Media Files**: `/srv/tracuu/media` → `/srv/media`

### Access the application
Open your browser and go to: `http://localhost:8000`

---

## Quick install
```bash
curl -fsSL https://raw.githubusercontent.com/q2kit/tracuu/refs/heads/main/install.sh | sh
```
