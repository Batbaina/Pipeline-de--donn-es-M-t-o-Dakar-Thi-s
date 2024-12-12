from flask import Flask
import models.functions as func

app = Flask(__name__)

@app.route('/')
def hello_world():
    data = func.crawl()
    # func.insert(data)
    return data