#!/bin/sh

echo "Waiting for MongoDB..."
while ! nc -z mongo_db 27017; do
  sleep 1
done
echo "MongoDB started!"

# Run database initialization scripts
python database/init_mongo.py
python database/init_chroma.py

# Start FastAPI with Uvicorn
exec uvicorn api.main:app --host 0.0.0.0 --port 5001 --reload
