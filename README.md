# Sereact Task

## Overview
This project is a **FastAPI-based product matching system** that utilizes ONNX-based deep learning models and ChromaDB for vector search. It allows users to upload an image or provide a URL, and the system retrieves similar products using embeddings.

## Project Structure

```
- api/
   ├── main.py           # FastAPI application entry point
- artifacts/
   ├── clip_model_fp16.onnx  # Pre-trained ONNX model it will be created once you run the command
- data/
   ├── embeddings.json   # Precomputed embeddings for products
   ├── products.json     # Product metadata
- database/
   ├── chroma_crud.py    # ChromaDB operations for vector search
   ├── init_chroma.py    # Initializes ChromaDB with embeddings
   ├── init_mongo.py     # Initializes MongoDB with product data
   ├── mongo_crud.py     # MongoDB operations for product retrieval
- helper/
   ├── util.py           # Utility functions (e.g., image preprocessing)
- models/
   ├── model_loader.py   # Loads ONNX model for inference
- services/
   ├── match_service.py  # Core matching logic using embeddings and ChromaDB
- docker-compose.yml     # Docker configuration for MongoDB and FastAPI
- requirements.txt       # Required dependencies for the project
```

## Installation & Setup

### **1. Clone the Repository**
```sh
$ git clone <repo-url>
$ cd <project-folder>
```

### **2. Install Dependencies**
```sh
$ docker-compose up --build
```

### **3. Run the Application with Docker**
```sh
$ uvicorn api.main:app --reload
```

### **4. Run with Docker (Optional)**
```sh
$ docker-compose up --build
```

## API Endpoints

### **Match Products**
- **POST `/match`**: Upload an image or provide an image URL and text to get similar product matches.

### **Fetch Logs**
- **GET `/logs`**: Retrieve stored error logs from MongoDB.

## Technologies Used
- **FastAPI** - Web framework
- **MongoDB** - Product data storage
- **ChromaDB** - Vector search database
- **ONNXRuntime** - Model inference
- **Docker** - Containerized deployment

---

### Next Steps
Please provide details about each file so we can enhance this README with deeper explanations and examples.

