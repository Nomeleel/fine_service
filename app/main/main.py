from app.util import util
from app.config import appconfig
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

#TODO move to index.py as main entrance.
if __name__ == "__main__":
    app.run(debug=True, host=appconfig.HOST, port=appconfig.PORT)
