import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-large"
)

img_url = "https://scontent-fra3-2.cdninstagram.com/v/t39.30808-6/358415987_18205520332247854_4569687895624484068_n.jpg?stp=dst-jpg_e35_s1080x1080_sh0.08&_nc_ht=scontent-fra3-2.cdninstagram.com&_nc_cat=1&_nc_ohc=BdOCCzrK-UwAX_jaXZ5&edm=AJ9x6zYAAAAA&ccb=7-5&ig_cache_key=MzE0NDAxMzM3ODMxODM1NzczOA%3D%3D.2-ccb7-5&oh=00_AfCR0LRJwkEEzSm0W_fk_xx1dR0q89eN6Eg1mUo2UOAprw&oe=64B11595&_nc_sid=65462d"
raw_image = Image.open(requests.get(img_url, stream=True).raw).convert("RGB")

# conditional image captioning
text = "a photography of"
inputs = processor(raw_image, text, return_tensors="pt")

out = model.generate(**inputs)
print(processor.decode(out[0], skip_special_tokens=True))

# unconditional image captioning
inputs = processor(raw_image, return_tensors="pt")

out = model.generate(**inputs)
print(processor.decode(out[0], skip_special_tokens=True))
