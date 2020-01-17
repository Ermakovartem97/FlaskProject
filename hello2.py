import os
from flask import Flask, render_template, request
from flask import send_from_directory
from werkzeug.utils import secure_filename
import subprocess


UPLOAD_FOLDER = './jythonMusic/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


MAX_FILE_SIZE = 1024 * 1024 + 1

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/", methods=["POST", "GET"])
def upload_file():
    os.system('./jythonMusic/JEM.jar')
    args = {"method": "GET"}
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            args["method"] = "POST"
            #subprocess.call(["./jythonMusic/jython.sh", shell = True])#'./jythonMusic/project.py'
            #arg = './jythonMusic/project.py'
            #subprocess.check_call("./jythonMusic/jython.sh '%s'" % './jythonMusic/project.py', shell=True)
            with open('./jythonMusic/jython.sh', 'rb') as file:
                script = file.read()
            rc = subprocess.call(script, shell=True)

    return render_template("index.html", args = args)

@app.route('/getfile/<path:name>')
def getfile(name):
    try:
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename = name, as_attachment=True)
    except FileNotFoundError:
        abort(404)

if __name__ == "__main__":
    app.run(debug=True)



