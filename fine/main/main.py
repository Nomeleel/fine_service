from config import appconfig
from util import util
from module.sudoku.sudoku import Sudoku
from flask import Flask
from flask import jsonify
from flask import request
import os

app = Flask(__name__)


@app.route("/sudoku", methods=['POST'])
def sudoku():
    sudoku_str = tryGetValue('sudokuStr')
    image_file = tryGetValue('image', True)
    isSolved = False
    try:
        if not sudoku_str is None:
            isSolved, sudoku_str = Sudoku(sudoku_str=sudoku_str).execute()
        elif image_file and util.isImageByExtension(image_file.filename):
            isSolved, sudoku_str = Sudoku(image_source=image_file.read()).execute()
        else:
            raise Exception('400')
    except Exception as e:
        print(e)
    
    return jsonify(solved=isSolved, sudokuStr=sudoku_str)


def tryGetValue(key, isFile=False):
    value = None
    try:
        if isFile:
            value = request.files[key]
        else:
            value = request.form[key]

    except Exception as e:
        print(e)

    return value
