FROM node:20-alpine AS config-builder
WORKDIR /app
COPY . .
RUN node scripts/render_site_config.mjs .env.production > site-config.js

FROM nginxinc/nginx-unprivileged:1.27-alpine
COPY deploy/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=config-builder /app/index.html /usr/share/nginx/html/index.html
COPY --from=config-builder /app/styles.css /usr/share/nginx/html/styles.css
COPY --from=config-builder /app/main.js /usr/share/nginx/html/main.js
COPY --from=config-builder /app/site-config.js /usr/share/nginx/html/site-config.js
COPY --from=config-builder /app/robots.txt /usr/share/nginx/html/robots.txt
COPY --from=config-builder /app/sitemap.xml /usr/share/nginx/html/sitemap.xml
COPY --from=config-builder /app/site.webmanifest /usr/share/nginx/html/site.webmanifest
COPY --from=config-builder /app/favicon.ico /usr/share/nginx/html/favicon.ico
COPY --from=config-builder /app/apple-touch-icon.png /usr/share/nginx/html/apple-touch-icon.png
COPY --from=config-builder /app/assets /usr/share/nginx/html/assets
EXPOSE 8080
