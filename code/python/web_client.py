import http.client
import json
import time

import sys

if len(sys.argv) >= 2:
    img_path = "./data/" + str(sys.argv[1])
else:
    img_path= "data/1mb.jpg"

conn = http.client.HTTPConnection('localhost:8080')

headers = {'Content-type': 'image/jpeg'}
# https://www.geeksforgeeks.org/http-headers-content-type/
# image/gif
# image/jpeg
# image/png
# image/tiff
# image/vnd.microsoft.icon
# image/x-icon
# image/vnd.djvu
# image/svg+xml

img = open(img_path, 'rb').read()
print("image binary size ", len(img))
for _ in range(20):
    start = time.time()
    # send http request with image and receive response
    conn.request('POST', '/', img, headers)
    response = conn.getresponse()
    print("PROCESSING TIME: ", time.time() - start)

# decode response
# print(json.loads(response.read().decode()))
# print(response.read().decode())