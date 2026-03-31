# ── Frontend Dockerfile ─────────────────────────────────────────────
# Stage 1: Build Tailwind CSS
FROM node:20-alpine AS builder

WORKDIR /app

# Install node dependencies (tailwindcss)
COPY package.json .
RUN npm install

# Copy all source files and build CSS
COPY . .
RUN npm run build:css

# ────────────────────────────────────────────────────────────────────
# Stage 2: Serve with Nginx
FROM nginx:alpine

# Remove default nginx page
RUN rm -rf /usr/share/nginx/html/*

# Copy built files from the builder stage
COPY --from=builder /app /usr/share/nginx/html

# Copy custom nginx config — sets default route to login.html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
