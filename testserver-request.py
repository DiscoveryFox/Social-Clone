import requests

image = requests.get('https://news.mit.edu/sites/default/files/images/202303/MIT-Python.png').content


url = 'http://192.168.0.207:5000/upload_image_post'

files = {'image': image}

response = requests.post(url, files=files)

print(response.text)