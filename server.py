from flask import Flask, send_from_directory
import random
import json

app = Flask(__name__)


@app.route("/")
def main():
    return send_from_directory('client/public', 'index.html')



@app.route("/test")
def test():
    print("test dziala")
    x = '{ "name":"John", "age":30, "city":"New York"}'
    return json.loads(x)

@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)


if __name__ == "__main__":
    app.run(debug=True)
