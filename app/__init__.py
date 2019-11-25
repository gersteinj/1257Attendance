from flask import Flask
from app import config
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
os.environ['AIRTABLE_API_KEY'] = config.API_KEY

from app import routes