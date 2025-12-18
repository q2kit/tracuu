#!/bin/bash

set -e

echo "==> Đang cài đặt server..."

if ! command -v nginx >/dev/null 2>&1; then
  echo "==> Đang cài nginx..."
  apt update -y
  apt install -y nginx
else
  echo "==> Nginx đã được cài."
fi

NGINX_CONF="/etc/nginx/sites-available/tracuu"
if [ ! -f "$NGINX_CONF" ]; then
  tee "$NGINX_CONF" > /dev/null <<EOF
server {
    listen 80;
    server_name tracuuhoadon247.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header    Host \$host;
        proxy_set_header    X-Real-IP \$remote_addr;
        proxy_set_header    X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF
else
  echo "==> File cấu hình nginx đã tồn tại."
fi

if [ -L /etc/nginx/sites-enabled/tracuu ]; then
  echo "==> Symlink đã tồn tại."
elif [ -e /etc/nginx/sites-enabled/tracuu ]; then
  echo "==> File tồn tại nhưng không phải symlink, đang xóa và tạo lại..."
  rm -f /etc/nginx/sites-enabled/tracuu
  ln -s /etc/nginx/sites-available/tracuu /etc/nginx/sites-enabled/
else
  echo "==> Tạo symlink mới..."
  ln -s /etc/nginx/sites-available/tracuu /etc/nginx/sites-enabled/
fi

nginx -t
systemctl restart nginx

if ! command -v docker >/dev/null 2>&1; then
  echo "==> Docker chưa được cài. Đang tiến hành cài đặt..."
  apt update -y
  apt install -y ca-certificates curl gnupg lsb-release

  install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  chmod a+r /etc/apt/keyrings/docker.gpg

  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

  apt update -y
  apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

  echo "==> Docker đã được cài đặt."
fi

# Chuẩn bị thư mục chứa dữ liệu
echo "==> Pull Docker image..."
docker pull q2kit/tracuu:production

touch /srv/tracuu/db.sqlite3
chown -R $(whoami):$(whoami) /srv/tracuu

if docker ps -a --format '{{.Names}}' | grep -Eq '^tracuu$'; then
  echo "==> Dừng container cũ..."
  docker stop tracuu
  docker rm tracuu
fi

echo "==> Chạy container..."
docker run -d -p 8000:80 --name tracuu \
  -v /srv/tracuu/db.sqlite3:/srv/db.sqlite3 \
  -v /srv/tracuu/.env:/srv/.env \
  q2kit/tracuu:production

echo "==> Migrate database..."
docker exec tracuu python3 manage.py migrate

echo "✅ Hoàn tất cài đặt!"
