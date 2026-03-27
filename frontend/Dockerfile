# # Build stage
# FROM node:20-slim AS builder

# WORKDIR /app

# # Copy package files
# COPY package.json package-lock.json* ./

# # Install dependencies
# RUN npm ci

# # Copy source code
# COPY . .

# # Build the application
# RUN npm run build

# # Production stage
# FROM nginx:alpine

# # Copy nginx configuration
# COPY nginx.conf /etc/nginx/nginx.conf

# # Copy built assets from builder
# COPY --from=builder /app/dist /usr/share/nginx/html

# # Create non-root user for nginx
# RUN addgroup -g 1000 appuser && adduser -D -u 1000 -G appuser appuser

# # Set permissions
# RUN chown -R appuser:appuser /usr/share/nginx/html && \
#     chown -R appuser:appuser /var/cache/nginx && \
#     chown -R appuser:appuser /var/log/nginx && \
#     touch /var/run/nginx.pid && \
#     chown appuser:appuser /var/run/nginx.pid

# USER appuser

# # Expose port 80
# EXPOSE 80

# # Start nginx
# CMD ["nginx", "-g", "daemon off;"]



# frontend/Dockerfile
# Build stage
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
# RUN npm ci --only=production
RUN npm ci

# Copy source code
COPY . .

# Build the app with production API URL
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

RUN npm run build

# Production stage with Nginx
FROM nginx:stable-alpine

# Copy built assets from build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]