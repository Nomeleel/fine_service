from config import appconfig
from util import util
from module.sudoku.sudoku import Sudoku
from flask import Flask
from flask import request
import os

app = Flask(__name__)


@app.route("/image", methods=['POST'])
@app.route("/sudoku", methods=['POST'])
def sudoku():
    image_file = request.files['image']
    if image_file and util.isImageByExtension(image_file.filename):
        Sudoku(image_file.read())
        
        return '200'
