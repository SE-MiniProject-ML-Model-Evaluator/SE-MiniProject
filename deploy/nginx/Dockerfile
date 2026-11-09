# Nginx reverse proxy with TLS (SR-04). Creates a self-signed certificate for local demos
# if no real certificate is mounted at /etc/nginx/certs.
FROM nginx:1.27-alpine
RUN apk add --no-cache openssl
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY make-cert.sh /docker-entrypoint.d/05-make-cert.sh
RUN chmod +x /docker-entrypoint.d/05-make-cert.sh
