import os
from flask import render_template, session
import requests
import json
import face_recognition
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
    

    for picture_b in pictures_bytes:
        try:
            image = base64.b64decode(picture_b["picture"], validate=True)
            with open(f"venv/static/uploads/self/me_img{picture_b['id']}.png", "wb") as f:
                f.write(image)
        except (binascii.Error, KeyError) as e:
            print(e)
    
def is_human(path):
    image = face_recognition.load_image_file(path)
    face_locations = face_recognition.face_encodings(image)
    if len(face_locations) <= 0:
        return 0

    elif len(face_locations) > 1:
        return 2

    return 1

def check_for_face(path, known_encodings): 
    try:   
        unknown_image = face_recognition.load_image_file(path)
        unknown_encoding = face_recognition.face_encodings(unknown_image)
        for face in unknown_encoding:
            print(face_recognition.face_distance(known_encodings, face))
            if any(face_recognition.compare_faces(known_encodings, face, tolerance=0.6)):
                return True
    except Exception as err:
        print(err)
        
    return False