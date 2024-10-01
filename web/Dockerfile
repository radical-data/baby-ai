# Step 1: Build the app with Node.js
FROM node:22-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Step 2: Serve the app using Node.js with adapter-node
FROM node:22-alpine
WORKDIR /app

# Copy built files and necessary package files
COPY --from=builder /app /app

# Install production dependencies
RUN npm ci --omit=dev

# Expose the port the app runs on (default for SvelteKit is 3000)
EXPOSE 3000

# Healthcheck to verify that the app is running
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD curl -f http://localhost:3000/ || exit 1

# Start the Node.js application
CMD ["node", "build"]