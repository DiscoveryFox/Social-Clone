from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import requests

url = "https://scontent-fra3-2.cdninstagram.com/v/t39.30808-6/358415987_18205520332247854_4569687895624484068_n.jpg?stp=dst-jpg_e35_s1080x1080_sh0.08&_nc_ht=scontent-fra3-2.cdninstagram.com&_nc_cat=1&_nc_ohc=BdOCCzrK-UwAX_jaXZ5&edm=AJ9x6zYAAAAA&ccb=7-5&ig_cache_key=MzE0NDAxMzM3ODMxODM1NzczOA%3D%3D.2-ccb7-5&oh=00_AfCR0LRJwkEEzSm0W_fk_xx1dR0q89eN6Eg1mUo2UOAprw&oe=64B11595&_nc_sid=65462d"
image = Image.open(requests.get(url, stream=True).raw)

processor = ViTImageProcessor.from_pretrained("google/vit-base-patch16-224")
model = ViTForImageClassification.from_pretrained("google/vit-base-patch16-224")

inputs = processor(images=image, return_tensors="pt")
outputs = model(**inputs)
logits = outputs.logits
# model predicts one of the 1000 ImageNet classes
predicted_class_idx = logits.argmax(-1).item()
print("Predicted class:", model.config.id2label[predicted_class_idx])
