FROM python:3.11-slim

WORKDIR /app

# ✅ Copie depuis le contexte (backend/) - PAS besoin de "backend/"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# ✅ Port 8000 (standard Railway) - fonctionne même si vous utilisez 8080 en local
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]