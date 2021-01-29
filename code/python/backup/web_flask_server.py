# https://gist.github.com/kylehounslow/767fb72fde2ebdd010a0bf4242371594
from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2

# Initialize the Flask application
app = Flask(__name__)

import logging

# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    r = request

    app.logger.info("test")
    size = len(r.data)
    # logger.info("Received sized : %s" % size)

    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # do some fancy processing here....

    # build a response dict to send back to client
    response = {'message': 'image received. size={}, img-format={}x{}'.format(size, img.shape[1], img.shape[0])
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


# start flask app
app.run(host="0.0.0.0", port=5000)