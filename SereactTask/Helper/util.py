import numpy as np


def preprocess_image(image):
    image = image.resize((224, 224))
    image_array = np.array(image).astype(np.float32) / 255
    image_array = image_array.transpose(2, 0, 1)[None, :]
    return image_array.astype(np.float16)
