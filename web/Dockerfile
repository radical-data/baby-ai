# Step 1: Build the app with Node.js
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Step 2: Serve with nginx
FROM nginx:alpine
# Install curl for the health check
RUN apk --no-cache add curl
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -f http://localhost:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]