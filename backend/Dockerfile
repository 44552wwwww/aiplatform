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

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
