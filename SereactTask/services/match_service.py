import requests
import onnxruntime as ort
from PIL import Image
from io import BytesIO
import numpy as np
import os
from helper.util import preprocess_image
from database.chroma_crud import search_embeddings
from database.mongo_crud import get_product_from_db
from transformers import CLIPTokenizer

base_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_path, "../artifacts/clip_model_fp16-new.onnx")

session = ort.InferenceSession(file_path)
tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-base-patch32")


def get_product(file, image_url, text):
    if file:
        image = Image.open(file.file)
    elif image_url:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
    else:
        return {"error": "No image provided"}

    image_tensor = preprocess_image(image)

    if text:
        text_inputs = tokenizer(text, padding="max_length", truncation=True, max_length=3, return_tensors="np")
        input_ids = text_inputs["input_ids"].astype(np.int64)  # Ensure int64 format
    else:
        input_ids = np.zeros((1, 3), dtype=np.int64)  # Dummy input of shape (1,3) for compatibility

    embedding = session.run(None, {"pixel_values": image_tensor, "input_ids": input_ids})[-1]

    similar_products = search_embeddings(embedding, n_results=10)
    match_product = []

    for product_id in similar_products["ids"][0]:
        metadata = get_product_from_db(product_id)
        match_product.append(metadata)

    return {"matches": match_product}
