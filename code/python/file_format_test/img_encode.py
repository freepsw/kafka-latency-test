import sys
import time

import cv2
import base64

# 0. original file size # 1,093,957 byte(1mb.jpg)
file_name = "1mb"
file_ext = ".jpg"
file_path = "../data/"

# 1. Byte size using cv2 api
im = cv2.imread(file_path + file_name + file_ext)

# 아래와 같이 메모리에 로딩된 사이즈가 커지는 이유는 이미지의 압축이 해제되어 전체 데이터(m x n x 3 bytes)를 로딩하게 된다.
# 하지만 실제 디스크에 저장된 이미지는 압축 알고리즘 및 압축률에 따라서 사이즈가 훨씬 작을 것이다.
# https://stackoverflow.com/questions/53607289/jpeg-image-memory-byte-size-from-opencv-imread-doesnt-seem-right
print("Image loaded into memory size(mb) :", round(sys.getsizeof(im) / (1024 * 1024), 2), "mb")
print("Image loaded into memory size(bytes) :", sys.getsizeof(im), "bytes")

print("Image loaded into memory size(bytes) :", len(im.tobytes())) # size : 18,450,000 byte(1mb.byte, increased 16x)

with open(file_path + '/enc/' + file_name +'.cv2.byte.jpg', 'wb') as f:
    f.write(im.tobytes())

# 2. Byte size using file api
image = open(file_path + file_name + file_ext, 'rb') # open binary file in read mode
image_read = image.read()
size = len(image_read)
print("Image Original file size :", size) # size : 1,093,957 byte (o
with open(file_path + '/enc/' + file_name + '.file.byte', 'wb') as f:
    f.write(image_read)

start = time.time()
b64_enc = base64.b64encode(image_read)
print("B64 encode Time : ", time.time() - start)

size = len(b64_enc)
print("Image Base64 file size :", size) #
with open(file_path + '/enc/' + file_name + '.b64', 'wb') as f:
    f.write(b64_enc)

image_64_decode = base64.decodebytes(b64_enc)
image_result = open(file_path + '/enc/' + file_name + '.b64.jpg', 'wb') # create a writable image and write the decoding result
image_result.write(image_64_decode)