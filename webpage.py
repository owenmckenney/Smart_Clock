from flask import Flask, render_template, current_app, g, request, jsonify, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
