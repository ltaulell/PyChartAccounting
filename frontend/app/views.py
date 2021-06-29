from flask import Flask, request, render_template, url_for, redirect, json, jsonify
import app.utils as utils
from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')