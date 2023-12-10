import os
from flask import render_template, session
import requests
import json
import cv2
import base64, binascii
from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def call_api(method, body):
    URL = f"https://tyrian-throats.000webhostapp.com/{method}.php"
    #URL = f"https://tyrian-throats.000webhostapp.com/get_all_users.php"
    #headers = {'Content-Type': 'application/json'}

    rows = requests.post(URL, data=body, json=body)
    if rows.status_code == 200:
        #print(rows.text)
        return rows.text
    else:
        return rows.status_code
    
def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError as e:
    return False
  return True

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_user_pics(user_id):
    folder = 'venv/static/uploads/self/'

    # Remove existing files in the folder
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

    # Retrieve pictures for the specified user_id
    body = {
        "user_id": user_id
    }

    pictures_bytes = json.loads(call_api("get_all_pics_by_user", body))

    i = 1
    for picture_b in pictures_bytes:
        try:
            image = base64.b64decode(picture_b["picture"], validate=True)
            with open(f"venv/static/uploads/self/me_img{i}.png", "wb") as f:
                f.write(image)
        except (binascii.Error, KeyError) as e:
            print(e)
        i += 1
    
def is_human(path):
    img = cv2.imread(path)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    face = face_classifier.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
    )
    if len(face) > 0:
        return True  # Faces detected
    else:
        return False  # No faces detected