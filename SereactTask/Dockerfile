FROM python

WORKDIR /app

COPY . /app

ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y netcat-openbsd

RUN pip install --no-cache-dir -r requirements.txt

RUN python models/model_loader.py

ENV MONGO_URI=mongodb://mongo_db:27017/product_db
ENV CHROMA_PATH=/database/chroma

COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the FastAPI port
EXPOSE 5001

# Use the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]

# Fallback CMD (will be ignored if ENTRYPOINT runs correctly)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "5001", "--reload"]
