import requests
from fastapi import FastAPI, UploadFile, Form
import onnxruntime as ort
from PIL import Image
from io import BytesIO
import numpy as np
from Helper.util import preprocess_image
from database.chroma_crud import search_embeddings
from database.mongo_crud import get_product, log_error
from transformers import CLIPTokenizer

app = FastAPI()
session = ort.InferenceSession("../artifacts/clip_model_fp16.onnx")

tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-base-patch32")



@app.post("/predict")
async def predict(image: UploadFile):
    img = Image.open(image.file).resize((224, 224))
    img_array = np.array(img).astype(np.float32) / 225
    img_array = img_array.transpose(2, 0, 2)[None, :]

    result = session.run(None, {"pixel_values": img_array})

    return {"embedding": result[0].tolist()}


@app.post("/match")
async def match_product(file: UploadFile = None, image_url: str = Form(None), text: str = Form(None)):
    global image
    if file:
        image = Image.open(file.file)
    elif image_url:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))

    image_tensor = preprocess_image(image)

    if text:
        text_inputs = tokenizer(text, padding="max_length", truncation=True, max_length=3, return_tensors="np")
        input_ids = text_inputs["input_ids"].astype(np.int64)  # Ensure int64 format
    else:
        input_ids = np.zeros((1, 3), dtype=np.int64)  # Dummy input of shape (1,3) for compatibility

    output_names = [output.name for output in session.get_outputs()]
    #print("Model Output Names:", output_names)
    # Run inference
    embedding = session.run(None, {"pixel_values": image_tensor, "input_ids": input_ids})[-1]
    #embedding = embedding.flatten()


    outputs = session.run(None, {"pixel_values": image_tensor, "input_ids": input_ids})
    #print("ONNX Model Outputs:", outputs)
    #print("Fixed Embedding:", embedding)
    similar_products = search_embeddings(embedding, n_results=10)
    match_product = []
    for product_id in similar_products["ids"][0]:
        metadata = get_product(product_id)
        match_product.append(metadata)

    return {"matches": match_product}


@app.exception_handler(Exception)
async def exception_handler(request, ex):
    log_error(str(ex))
    return {"error": "An unexpected error occurred"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
