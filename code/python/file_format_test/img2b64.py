import json
import base64
import argparse
import os
import shutil
import logging
from pathlib import Path


def convert():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", default="./data/", type=str)
    parser.add_argument("--file_name", default="3mb.jpg", type=str)
    parser.add_argument("--type", default="base64", type=str)
    args = parser.parse_args()
    file_path = args.file_path
    file_name = args.file_name
    file_type = args.type
    name = str(file_name)[0:-4]
    if not (os.path.isdir(file_path)):
        logging.info('wrong path, please input path and filename as --file_path, --file_name')

    # img_file = os.path.join(file_path, file_name)
    # print(img_file)
    with open(os.path.join(file_path, file_name), mode='rb') as file:
        ## jpg to binary
        img = file.read()
    ## binary to base64
    # encoding img by base64.encodebyte library and decode to utf-8 (makes img string)
    if file_type == 'binary':
        with open(os.path.join(file_path, name + '.json'), 'w') as f:
            res = {'instnaces': list(img)}
            json.dump(res, f, ensure_ascii=False)
    elif file_type == 'base64':
        with open(os.path.join(file_path, name + '.json'), 'w') as f:
            string = base64.encodebytes(img).decode('utf-8')
            res = {'instances': [{'image': {'b64': string}}]}
            json.dump(res, f, ensure_ascii=False)
    return res


if __name__ == "__main__":
    convert()