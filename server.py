import os
import io
import base64
import json

import cv2
from PIL import Image
from flask import Flask, request , make_response, Response
from flask_cors import CORS,cross_origin

import Annotator.screenshot_analysis as analysis

# Initialize the Flask application
app = Flask(__name__)
## for allowing cors origin
cors = CORS(app, allow_headers='Content-Type', CORS_SEND_WILDCARD=True)

## Allowed extensions for image upload
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])



def allowed_file(filename):
    """ This function is for checking the valid domain of the file"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
# route http posts to this method
@app.route('/api/test', methods=['POST'])
@cross_origin(origins='*', send_wildcard=True)
def annotate_uploaded_image(): 
    
    if 'file' not in request.files:
        data = {'status' : 'Invalid Request'}
        return Response(json.dumps(data), status=400, mimetype='application/json')
    
    file = request.files['file']

    if file.filename == '':
        
        data = {'status' : 'No file selected'}
        return Response(json.dumps(data), status=415, mimetype='application/json')

    if file and allowed_file(file.filename):
        
        image_content = file.read()
        coordinates = analysis.annotate_screenshot(image_content,file.filename)
        # img = Image.fromarray(annotated_image.astype("uint8"))
        # rawBytes = io.BytesIO()
        # img.save(rawBytes, "JPEG")
        # rawBytes.seek(0)
        # img_base64 = base64.b64encode(rawBytes.read())
        # data = {"status" : str(img_base64)}
        return Response(json.dumps(coordinates), status=200, mimetype='application/json')
    else:
        data = {'status' : 'Invalid file type'}
        return Response(json.dumps(data), status=415, mimetype='application/json')

# start flask app
if __name__ == "__main__":
    
    ## Change debug to False when deployed to production
    app.run(debug=True,host="localhost", port=5000)