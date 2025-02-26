import os
import torch
import onnx
from transformers import CLIPProcessor, CLIPModel
from onnxmltools.utils.float16_converter import convert_float_to_float16

# Define the path to the artifacts directory (one level above)
ARTIFACTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "artifacts")
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

# Load CLIP model
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")

# Save PyTorch model in artifacts folder
model_path = os.path.join(ARTIFACTS_DIR, "clip_onnx")
model.save_pretrained(model_path)

# Dummy input for ONNX export
dummy_input = {
    "pixel_values": torch.rand(1, 3, 224, 224),
    "input_ids": torch.tensor([[0, 1, 2]])
}

# Define ONNX model path
onnx_model_path = os.path.join(ARTIFACTS_DIR, "clip_model.onnx")

# Export to ONNX
torch.onnx.export(
    model,
    (dummy_input["input_ids"], dummy_input["pixel_values"]),
    onnx_model_path,
    input_names=["input_ids", "pixel_values"],
    output_names=["output"],
    dynamic_axes={"input_ids": {0: "batch_size"}, "pixel_values": {0: "batch_size"}}
)

print(f"Model converted to ONNX and saved at {onnx_model_path}")

# Load original ONNX model
model_fp32 = onnx.load(onnx_model_path)

# Convert to FP16
model_fp16 = convert_float_to_float16(model_fp32)

# Define FP16 model path
quantized_model_path = os.path.join(ARTIFACTS_DIR, "clip_model_fp16-new.onnx")

# Save quantized model
onnx.save(model_fp16, quantized_model_path)

print(f"FP16 quantization completed! Quantized model saved at {quantized_model_path}")
