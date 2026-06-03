import os
import time
from flask import Flask, render_template, request, session, request, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import jsonify
from collections import defaultdict, deque
import random
from pathlib import Path

from app.parser import KmlRouteParser

from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)
app.secret_key = "CHAquest.remote_aNGE_THIS"
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB

app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)

# per-IP request timestamps
request_log = defaultdict(deque)

CHALLENGE_THRESHOLD = 1      # max 1 request
WINDOW_SECONDS = 60

UPLOAD_DIR = "/app/uploads"
LOG_FILE = "/app/logs/requests.log"
#DATA_FILE = "/app/data/rate_limits.sqlite3"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(str(Path(LOG_FILE).parent), exist_ok=True)

# -----------------------
# Rate limiting (PRODUCTION SAFE)
# -----------------------
limiter = Limiter(
    get_remote_address,
    storage_uri="redis://redis:6379/0",
    app=app,
    default_limits=["30 per minute"]
)

def is_abusive(ip):
    now = time.time()
    q = request_log[ip]

    # remove old requests outside 60 sec window
    while q and now - q[0] > WINDOW_SECONDS:
        q.popleft()

    q.append(now)

    return len(q) > CHALLENGE_THRESHOLD

def generate_challenge():
    a = random.randint(10, 99)
    b = random.randint(10, 99)

    session["answer"] = a + b
    return f"{a} + {b}"


# -----------------------
# Simple request logger
# -----------------------
def log_request():
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.time()} {request.remote_addr} {request.path}\n")


# -----------------------
# JS challenge
# -----------------------
def generate_challenge():
    import random
    a, b = random.randint(10, 99), random.randint(10, 99)
    session["answer"] = a + b
    return f"{a} + {b}"


# -----------------------
# Routes
# -----------------------
@app.route("/", methods=["GET"])
def index():
    log_request()
    return render_template("index.html")

@app.route("/debug")
def debug():
    return {
        "X-Script-Name": request.headers.get("X-Script-Name"),
        "X-Forwarded-Prefix": request.headers.get("X-Forwarded-Prefix"),
        "SCRIPT_NAME": request.environ.get("SCRIPT_NAME"),
        "PATH_INFO": request.environ.get("PATH_INFO"),
        "script_name": request.environ.get("SCRIPT_NAME"),
        "url_root": request.url_root,
        "upload_url": url_for("upload"),
    }

@app.route("/upload", methods=["POST"])
@limiter.limit("10 per minute")
def upload():

    ip = request.remote_addr

    if is_abusive(ip) and not session.get("verified"):
        return jsonify({
            "challenge_required": True,
            "question": generate_challenge()
        }), 429

    file = request.files["file"]
    path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(path)

    parser = KmlRouteParser(path)
    parser.load()

    points = parser.get_points()
    url = parser.get_google_maps_url(use_names=True)

    return jsonify({
        "challenge_required": False,
        "url": url,
        "points": points
    })

'''
@app.route("/challenge", methods=["GET", "POST"])
def challenge():

    if request.method == "POST":
        if int(request.form["answer"]) == session.get("answer"):
            session["verified"] = True
            return {"ok": True}
        return {"ok": False}, 403

    return render_template(
        "challenge.html",
        question=generate_challenge()
    )
'''
@app.route("/challenge", methods=["POST"])
def verify():

    user_answer = int(request.form["answer"])

    if user_answer == session.get("answer"):
        session["verified"] = True
        return {"ok": True}

    return {"ok": False}, 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)