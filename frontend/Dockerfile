# =============================================================================
# Dockerfile cho Cognivasc Frontend (React + Vite)
# =============================================================================

# Multi-stage build để tối ưu kích thước
FROM node:18-alpine AS builder

# Metadata
LABEL maintainer="Cognivasc Team"
LABEL description="Cognivasc Frontend"
LABEL version="1.0.0"

# Thiết lập working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Cài đặt dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build ứng dụng
RUN npm run build

# Production stage
FROM nginx:alpine AS production

# Metadata
LABEL maintainer="Cognivasc Team"
LABEL description="Cognivasc Frontend Production"
LABEL version="1.0.0"

# Copy built files từ builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Tạo user không phải root
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Set permissions
RUN chown -R nextjs:nodejs /usr/share/nginx/html && \
    chown -R nextjs:nodejs /var/cache/nginx && \
    chown -R nextjs:nodejs /var/log/nginx && \
    chown -R nextjs:nodejs /etc/nginx/conf.d

# Tạo thư mục cho nginx pid
RUN mkdir -p /var/run/nginx && \
    chown -R nextjs:nodejs /var/run/nginx

# Chuyển sang user không phải root
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
