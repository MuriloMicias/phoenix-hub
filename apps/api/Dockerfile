# Stage 1 — build frontend with Node
FROM node:18-alpine AS web-build
WORKDIR /build
# Install dependencies and build
COPY apps/web/package.json apps/web/package-lock.json* ./  # package-lock optional
COPY apps/web/ ./apps/web/
# adjust working dir to apps/web for install
WORKDIR /build/apps/web
RUN npm ci --silent || npm install --silent
RUN npm run build

# Stage 2 — python runtime
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app

# Copy requirements and install
COPY apps/api/requirements.txt ./requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY apps/api/src ./src

# Copy frontend build into backend static directory
# Vite outputs to /build/apps/web/dist, copy to /app/src/static
COPY --from=web-build /build/apps/web/dist ./src/static

# Create a non-root user and give ownership to /app
RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && chown -R appuser:appuser /app

# Run as non-root
USER appuser

EXPOSE 8000

# Use shell form so $PORT is expanded by the shell, with a default fallback
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --log-level info --proxy-headers"]
