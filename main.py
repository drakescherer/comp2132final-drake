from flask import Flask, jsonify, render_template, request, redirect, url_for, make_response, abort, flash, Response, send_from_directory
from waitress import serve
import os
import logging
from dotenv import load_dotenv
from datetime import datetime, timedelta
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
load_dotenv()
app = Flask(__name__)
maintenance_mode = False

@app.route('/')
def home():
    return render_template('project.html')

@app.route('/assets/hangman_words.json')
def hangman_words():
    return send_from_directory('assets', 'hangman_words.json')


@app.before_request
def log_request_info():
    current_time = datetime.now()
    current_time_formatted = current_time.strftime('%m/%d %H:%M:%S')
    logging.info(f"{current_time_formatted} - {request.headers.get('X-Real-IP')} - {request.method} {request.path}")
    if maintenance_mode:
        if request.endpoint not in ['maintenance', 'static']:
            return redirect(url_for('maintenance'))

@app.errorhandler(404)
def page_not_found(e):
    return "", 404

@app.errorhandler(413)
def request_entity_too_large(e):
    flash("Sorry, your upload was too big! Max upload size is 10MB. Code: 413", 'error')
    return redirect(url_for("home"))

@app.errorhandler(429)
def too_many_requests(e):
    flash(f"Too many requests, Code: 429", 'error')
    return redirect(url_for("home"))

@app.errorhandler(500)
def internal_server_error(e):
    flash("Internal Server Error, please report this so we can fix it!", 'error')
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.secret_key = os.getenv("SECRET_KEY_FLASK")
    if os.getenv('SECRET_KEY_FLASK') == 'ThisSiteIsNotLive':
        print(f"SITE KEY NOT SETUP, DO NOT PUSH THIS TO A LIVE SERVER!!!!!")
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)
    serve(app, host='0.0.0.0', port=4200, threads=4)
