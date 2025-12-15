# Tracuu Application

## Docker Setup

### Build the Docker image
```bash
docker build -t tracuu .
```

### Run the Docker container
```bash
docker run -p 8000:80 --name tracuu \
  -v /srv/tracuu/.env:/srv/.env \
  -v /srv/tracuu/db.sqlite3:/srv/db.sqlite3 \
  tracuu
```

### Volume Mounts
- **Environment Variables**: `/srv/tracuu/.env` → `/srv/.env`
- **Database**: `/srv/tracuu/db.sqlite3` → `/srv/db.sqlite3`

### Access the application
Open your browser and go to: `http://localhost:8000`

---

## Quick install
```bash
curl -fsSL https://install.tracuuhoadon247.com/install.sh | sh
```
