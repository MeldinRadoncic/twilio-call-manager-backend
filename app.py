from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__) 



@app.route('/')
def testing():
    return 'Hello Twilio'


if __name__ == '__main__':
    # Run the app with debug mode on
    app.run()
