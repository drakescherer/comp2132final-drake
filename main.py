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
# limiter = Limiter(
#     get_remote_address,
#     app=app,
#     default_limits=["1000 per day", "200 per hour"],
#     storage_uri=f"redis://:{os.getenv('REDIS_PASS')}@192.168.1.198:6379/0",
# )
# limiter.init_app(app)
maintenance_mode = False

@app.route('/')
def home():
    # Changed this as the menu has not been setup yet.
    return render_template('project.html')

@app.route('/assets/hangman_words.json')
def hangman_words():
    return send_from_directory('assets', 'hangman_words.json')


@app.before_request
def log_request_info():
    current_time = datetime.now()
    current_time_formatted = current_time.strftime('%m/%d %H:%M:%S')
    logging.info(f"{current_time_formatted} - {request.headers.get('X-Real-IP')} - {request.method} {request.path}")
    # if request.headers.get('X-Real-IP') != '66.183.230.150':
    #     print(f"rejecting outside IP")
    #     return "", 404
    if maintenance_mode:
        if request.endpoint not in ['maintenance', 'static']:
            return redirect(url_for('maintenance'))

# @app.route('/robots.txt')
# def robots_txt():
#     robots_content = """
#                         User-agent: *
#                         Allow: /
#                      """
#
#     return Response(robots_content, mimetype='text/plain')

@app.errorhandler(404)
def page_not_found(e):
    return "", 404
    # flash("Page not found, Code: 404.", 'error')
    # return redirect(url_for("home"))

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
