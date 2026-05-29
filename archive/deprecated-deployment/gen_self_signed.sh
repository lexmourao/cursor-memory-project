#!/usr/bin/env bash
set -euo pipefail

CERT_DIR=nginx/certs
mkdir -p $CERT_DIR
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -subj "/CN=localhost" \
  -keyout $CERT_DIR/server.key -out $CERT_DIR/server.crt

HTPASS=nginx/htpasswd
read -p "Create basic auth user: " USER
read -s -p "Password: " PASS
printf "\n"
htpasswd -cb $HTPASS "$USER" "$PASS"

echo "Certificates and htpasswd generated." 