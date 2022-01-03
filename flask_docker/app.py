from flask import Flask, Response, request
import math
import subprocess


app = Flask(__name__, static_folder="/usr/src/app/volume/")


@app.route('/', methods=['GET'])
def index():
    res = Response("Hello world", 200)
    return res


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        try:
            target = "/usr/src/app/volume/uploaded"
            file = request.files['file']
            file.save(target)
            return Response("Success", 200)
        except:
            return Response("Error", 400)
    else:
        return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/checkPrime', methods=['GET'])
def checkPrime():
    try:
        number = int(request.args.get('number'))
        is_prime = lambda x: all([x % i != 0 for i in range(2, int(math.sqrt(x))+1)])
        result = is_prime(number)
        return Response(str(result), 200)
    except:
        return Response("Error", 400)


@app.route('/storeOnDisk', methods=['GET'])
def storeOnDisk():
    try:
        amount = int(request.args.get('amount'))
        if amount > 500 or amount <= 0:
            return Response("Invalid amount")
        command = f"dd if=/dev/zero of=./outfile bs={amount}M count=1".split(" ")
        result = subprocess.run(command, capture_output=True).stderr.decode().replace("\n", "</br>")
        return Response(result, 200)
    except:
        return Response("Error", 400)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
