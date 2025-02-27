# Sereact Task

## Overview
This project is a **FastAPI-based product matching system** that utilizes ONNX-based deep learning models and ChromaDB for vector search. It allows users to upload an image or provide a URL, and the system retrieves similar products using embeddings.

## Prerequisites
- **Docker** must be installed on your system. You can download it from [Docker's official website](https://www.docker.com/).

## Project Structure

```
- api/
   ├── main.py           # FastAPI application entry point
- artifacts/
   ├── clip_model_fp16.onnx  # Pre-trained ONNX model (if applicable)
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
   ├── model_loader.py   # Loads and quantizes ONNX model for inference
- services/
   ├── match_service.py  # Core matching logic using embeddings and ChromaDB
- scripts/
   ├── entrypoint.sh     # Script to initialize databases and start FastAPI
- docker-compose.yml     # Docker configuration for MongoDB, ChromaDB, and FastAPI
- Dockerfile             # Defines the container for FastAPI
- requirements.txt       # Required dependencies for the project
```

## Installation & Setup

### **1. Clone the Repository**
```sh
$ git clone https://github.com/farrukh-ahmed/sereact_task.git
$ cd SereactTask
```

### **2. Run the Application with Docker**
```sh
$ docker-compose up --build
```

## Docker Setup & Execution Flow

1. **Dependency Installation**
   - The `Dockerfile` sets up the environment by installing dependencies from `requirements.txt`.
   - It also loads and quantizes the ONNX model for inference using `model_loader.py`.
   
2. **Model Loading and Quantization**
   - The `model_loader.py` script downloads the CLIP model from Hugging Face.
   - The model is converted to ONNX format and saved in the `artifacts/` directory.
   - The ONNX model is further optimized by quantizing it to FP16 format for better performance.

3. **Database Initialization**
   - The `entrypoint.sh` script waits for MongoDB to start.
   - It then initializes MongoDB and ChromaDB using `init_mongo.py` and `init_chroma.py` (which load dummy data).

4. **FastAPI Server Startup**
   - After database initialization, FastAPI is launched using Uvicorn.
   
## API Endpoints

### **Match Products**
- **POST `/match`**
  - **Description**: Upload an image or provide an image URL and text to get similar product matches.
  - **Request Parameters**:
    - `file` (optional): Image file upload.
    - `image_url` (optional): URL of an image.
    - `text` (optional): Text input for additional matching criteria.
  - **Response**: Returns a list of matched products.
  - **Example Request**:
    ```sh
    curl -X POST "http://localhost:5001/match" \
         -F "image_url=https://example.com/sample.jpg" \
         -F "text=red sneakers"
    ```

### **Fetch Logs**
- **GET `/logs`**
  - **Description**: Retrieve stored error logs from MongoDB.
  - **Response**: Returns a JSON object containing logged errors.
  - **Example Request**:
    ```sh
    curl -X GET "http://localhost:5001/logs"
    ```

## Technologies Used
- **FastAPI** - Web framework
- **MongoDB** - Product data storage
- **ChromaDB** - Vector search database
- **ONNXRuntime** - Model inference
- **Docker** - Containerized deployment

---



