import base64
import json, os
from flask import Blueprint, render_template, Request, Response

from cloud_common.cc.google import storage
from cloud_common.cc.google import env_vars
from .utils.response import error_response


MEDIUM_FILE_SUFFIX = "_medium"

viewimage_bp = Blueprint('viewimage_bp', __name__)

@viewimage_bp.route("/viewImage/<imageData>", methods=['GET'])
def viewimage(imageData):
    imageDataString = base64.b64decode(imageData)
    imageObject = json.loads(imageDataString.decode('utf-8'))
    filename = imageObject['i'].split('/')[-1]

    # Find files with the filename - .png as a prefix
    file_prefix = filename.split('.')[0]
    bucket = storage.storage_client.get_bucket(env_vars.cs_bucket)
    blob_list = list(bucket.list_blobs(prefix=file_prefix))

    # Now look for the _medium version... 
    # if it exists then pass that to the view.
    found = False
    for blob in blob_list:
        if MEDIUM_FILE_SUFFIX in blob.name:
            imageObject['i'] = imageObject['i'].replace(filename, blob.name)
            found = True
            break
    if not found:
        return error_response(message='Invalid URL.')

    # file is in API/templates/
    return render_template('viewImage.html', imageFile=imageObject['i'], 
            imageText=imageObject['t'])

