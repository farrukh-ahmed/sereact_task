import requests
from fastapi import FastAPI, UploadFile, Form
from database.mongo_crud import log_error
from services.match_service import get_product

app = FastAPI()


@app.post("/match")
async def match_product(file: UploadFile = None, image_url: str = Form(None), text: str = Form(None)):
    return get_product(file, image_url, text)


@app.exception_handler(Exception)
async def exception_handler(request, ex):
    log_error(str(ex))
    return {"error": "An unexpected error occurred"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
