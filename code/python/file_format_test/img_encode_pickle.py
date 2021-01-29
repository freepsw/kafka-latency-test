import cv2
import pickle

# 0. original file size # 1,093,957 byte(1mb.jpg)
file_name = "1mb"
file_ext = ".jpg"
file_path = "../data/"

# 1. Byte size using cv2 api
im = cv2.imread(file_path + file_name + file_ext)

# Write to file.
file = open("../data/data.pkl", "wb")
# size = len(file.tobytes())
# print("Byte size ", size) # size : 18,450,000 byte(1mb.byte, increased 16x)
pickle.dump(im, file)

file.close()

file = open("../data/data.pkl", "rb")
image1 = pickle.load(file)
file.close()