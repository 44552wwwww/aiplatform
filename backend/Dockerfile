FROM python:3.12-slim

WORKDIR /app

# Copy from project root context (docker-compose build context = .)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ .

# Copy skills/ to /skills/ (matches _resolve_skills_dir: 4 parents up from
# /app/app/registry/ = / + "skills" = /skills)
COPY skills/ /skills/

# Entrypoint: run DB migration then start server
COPY backend/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
