#! /usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import os
from flask import Flask, render_template, request
from flask import send_from_directory, send_file
from werkzeug.utils import secure_filename
import subprocess

UPLOAD_FOLDER = './jythonMusic/'
ALLOWED_EXTENSIONS = set(['txt', 'jpg', 'jpeg'])

MAX_FILE_SIZE = 1024 * 1024 + 1

source_filename = ''

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=["POST", "GET"])
def upload_file():
#    os.system('./jythonMusic/JEM.jar')
    args = {"method": "GET"}
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            if file.filename.rsplit('.', 1)[1] == 'txt':
                namepr = 'project.py'
            else:
                namepr = 'project2.py'
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            source = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            output = source.rsplit("/", 1)[1].rsplit(".", 1)[0] + '.' + "mid"
            output_filename = app.config['UPLOAD_FOLDER'] + output
            print(source)
            print(output_filename)
            args["method"] = "POST"
            args["output"] = output
            #subprocess.call(["./jythonMusic/jython.sh", shell = True])#'./jythonMusic/project.py'
            #arg = './jythonMusic/project.py'
            #subprocess.check_call("./jythonMusic/jython.sh '%s'" % './jythonMusic/project.py', shell=True)
            arg = source + ';' + output_filename
            subprocess.call("./jythonMusic/jython.sh './jythonMusic/"+namepr+"' arg '%s'" % arg, shell=True)
            #with open('./jythonMusic/jython.sh', 'rb') as file:
            #    script = file.read()
            #rc = subprocess.call(script, shell=True)

    return render_template("index.new.html", args = args)

@app.route('/images/<filename>')
def images(filename):
    image = './templates/images/' + filename
    dirname = './templates/images/'
    
    if os.path.exists(image):
        return send_from_directory(dirname, filename = filename)
    else:
        print("File '%s' not found" % image)

@app.route('/getfile/<path:name>')
def getfile(name):
    try:
        filename = app.config["UPLOAD_FOLDER"] + name
        
        if os.path.exists(filename):
            return send_from_directory(app.config["UPLOAD_FOLDER"], filename = name, as_attachment=True)
        else:
            print("File '%s' not found" % filename)
    except:
        exit(0)

if __name__ == "__main__":
    app.run(debug=True)
