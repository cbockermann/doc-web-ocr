# app.py
from flask import Flask, render_template, send_from_directory, redirect, url_for           # import flask
from flask import request
from os import listdir, makedirs
from os.path import isfile, join
import os.path, time
import subprocess
import os
import datetime
import hashlib
import docweb
import uuid
from docweb.ocr import ocr_from_file

def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d")

def modification_time(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t).strftime("%H:%M:%S")

def md5(xs):
	return (hashlib.md5(str(xs).encode('utf-8')).hexdigest())

app = Flask("DocWeb", static_folder='static')             # create an app instance


@app.route("/ocr",methods=["PUT"])
def ocr():
#	print("reading OCR data from {}".format(request.uri))
	data = request.data
	n_bytes = len(data)
	print(f"Request contains {n_bytes} of data")
	tmpId = str(uuid.uuid4())
	tmpFile = f"/tmp/ocr-input-{tmpId}"
	file = open(tmpFile, "wb")
	file.write(data)
	file.close()
#	print(f"Wrote {n_bytes} bytes to {tmpFile}")
	txt = ocr_from_file(tmpFile)
#	print(f"Text is: {txt}")
	os.remove(tmpFile)
	return txt

def setup():
    makedirs("data/.thumbs", exist_ok=True)
    makedirs("incoming/.thumbs", exist_ok=True)

if __name__ == "__main__":        # on running python app.py
    setup()
    app.run(host="0.0.0.0")                     # run the flask app
