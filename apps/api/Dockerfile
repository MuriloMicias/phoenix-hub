# Stage 1 — build frontend with Node
FROM node:18-alpine AS web-build
WORKDIR /build/apps/web
COPY apps/web/ ./
RUN npm install --silent
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
COPY --from=web-build /build/apps/web/dist ./src/static

# Create a non-root user and give ownership to /app
RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --log-level info --proxy-headers"]
