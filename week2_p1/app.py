from flask import Flask, render_template
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@app.route('/')
def hello_world():
    logger.debug('Enter Hello World')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)