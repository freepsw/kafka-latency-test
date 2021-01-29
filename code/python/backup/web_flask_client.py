from __future__ import print_function
import requests
import json
import cv2

addr = 'http://localhost:5000'
test_url = addr + '/api/test'
img_file = '../data/1mb.jpg'
# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

# img = cv2.imread(img_file)
# _, img_encoded = cv2.imencode('.jpg', img)
# encode image as jpeg
# print("image string size ", len(img_encoded.tostring()))
# response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)

img = open(img_file, 'rb').read()
print("image binary size ", len(img))
# send http request with image and receive response
response = requests.post(test_url, data=img, headers=headers)
# decode response
print(json.loads(response.text))

# expected output: {u'message': u'image received. size=124x124'}