from config import appconfig
from util import util
from flask import Flask
from flask import request
import os

app = Flask(__name__)


@app.route("/sudoku", methods=['POST'])
def sudoku():
    image_file = request.files['image']
    if image_file and util.isImageByExtension(image_file.filename):
        # Sudoku
        # 1. save
        #   image_file.save(os.path.join(file_path, util.uniqueName(image_file.filename)))
        # 2. cv read
        #   cv2.read() ???
        return '200'
