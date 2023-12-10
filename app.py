import zipfile
from PIL import Image
import base64
from urllib.request import urlopen
import json
import os
import face_recognition
from flask import Flask, redirect, render_template, request, send_file, send_from_directory, session
import bcrypt
from helpers import apology, call_api, login_required, allowed_file, load_user_pics, is_human, check_for_face
from flask_session import Session

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        
        folder = 'venv/static/uploads/choose/'
        # Remove existing files in the folder
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
        
        if "files[]" in request.files:   
            load_user_pics(session["user_id"])         
            uploaded_files = request.files.getlist('files[]')
            known_encodings = []
            for image_name in os.listdir('venv/static/uploads/self/'):
                me_path = f"venv/static/uploads/self/{image_name}"
                known_image = face_recognition.load_image_file(me_path)
                known_encoding = face_recognition.face_encodings(known_image)[0]
                known_encodings.append(known_encoding)
            i = 1
            for file in uploaded_files:
                # Process each file as needed
                if not allowed_file(file.filename):
                    return apology("Invalid file type. Please upload an image (png, jpg, jpeg)", 400)

                path = f"venv/static/uploads/choose/picture_{i}.png"
                file.save(path)
                
                if not check_for_face(path, known_encodings):
                    os.remove(path)
                    continue
                    
                i += 1
        
        return redirect("/uploaded")
    else:    
        return render_template("index.html")
    
@app.route("/download")
@login_required
def download():
    folder_path = "venv/static/uploads/choose/"
    zip_filename = "pics_with_me.zip"

    # Create a zip file
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            zipf.write(file_path, os.path.basename(file_path))

    zip_path = "C:\\GitHub\\cs50-final-project\\cs50-final-project\\pics_with_me.zip"
    return send_file(zip_path, download_name=zip_filename, as_attachment=True)

@app.route("/uploaded")
@login_required
def uploaded():
    image_names = os.listdir('venv/static/uploads/choose/')
    return render_template("choose_pics.html", image_names=image_names)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        user = request.form.get("username")
        pw = request.form.get("password")
        if not user:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not pw:
            return apology("must provide password", 403)
        
        params = {"user": user}
        rows = json.loads(call_api("get_user_by_username", params))
        hashed_pw = rows[0]["password"]
        
        # Ensure username exists and password is correct
        if len(rows) != 1 or not bcrypt.checkpw(pw.encode('utf-8'), hashed_pw.encode('utf-8')):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@app.route("/myPictures")
@login_required
def myPictures():
    load_user_pics(session["user_id"])
    image_names = os.listdir('venv/static/uploads/self/')
    return render_template("my_pictures.html", image_names=image_names)

@app.route("/delete_image", methods=["POST"])
@login_required
def deleteImg():
    name = request.form.get("image_name")
    body = {
        "id": int(name[6:len(name) - 4])
    }
    call_api("delete_image", body)
    return redirect("/profile")
    
@app.route("/uploadMe", methods=["GET", "POST"])
@login_required
def upload_me():
    if request.method == "POST":
        if "file" in request.files:
            image = request.files["file"]

            if allowed_file(image.filename):
                # Save the image
                image_path = "venv/static/uploads/self/" + image.filename
                image.save(image_path)

                # Read the image file as binary and encode as base64
                with open(image_path, "rb") as img_file:
                    img_string = base64.b64encode(img_file.read()).decode('utf-8')
                    
                result = is_human(image_path)
                if result == 0:
                    os.remove(image_path)
                    return apology("couldnt recognize human in picture", 404)
                
                elif result == 2:
                    os.remove(image_path)
                    return apology("provide a picture with only 1 face", 404)
                                    
                # Your API call or processing with the base64 string
                body = {
                    "user_id": int(session["user_id"]),
                    "pic": img_string
                }
                call_api("post_picture", body)

                # Return success or redirect as needed
                return redirect("/")
            else:
                return apology("Invalid file type. Please upload an image (png, jpg, jpeg)", 400)
    else:
        count = 0
        dir_path = "venv/static/uploads/self/"
        for path in os.listdir(dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(dir_path, path)):
                count += 1
                
        if count > 3:
            return apology("max amount of pictures is 3 (delete some in /myPictures)", 400)
        
        return render_template("upload_me.html")

@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()
    if request.method == "POST":
        # Ensure username was submitted
        pw = request.form.get("password")
        pw2 = request.form.get("confirmation")
        username = request.form.get("username")
        email = request.form.get("email")
        if not username:
            return apology("must provide username", 400)
        
        if not email:
            return apology("must provide email", 400)

        # Ensure password was submitted
        elif not pw or not pw2:
            return apology("must provide password", 400)

        # passwords matchs
        elif not pw == pw2:
            return apology("passwords dont match", 400)

        elif not any(char.isalpha() for char in pw):
            return apology("password must contain at least one letter", 403)

        # Ensure the password contains at least one number
        elif not any(char.isdigit() for char in pw):
            return apology("password must contain at least one number", 403)

        # Ensure the password is at least 8 characters long
        elif len(pw) < 8:
            return apology("password must be at least 8 characters long", 403)
        
        elif "@" not in email:
            return apology("email must contain @", 403)
        
        body = {
            "username": username,
            "pw": pw,
            "email": email,
            "user": username
        }
        
        if len(call_api("get_user_by_username", body)) > 6:
            return apology("username/email already exists", 403)
        
        call_api("post_user", body)
        id = json.loads(call_api("get_user_by_username", body))[0]['id']
        
        
        #IMAGE HANDLING
        if "file" in request.files:
            image = request.files["file"]

            if allowed_file(image.filename):
                # Save the image
                image_path = "venv/static/uploads/self/" + image.filename
                image.save(image_path)

                # Read the image file as binary and encode as base64
                with open(image_path, "rb") as img_file:
                    img_string = base64.b64encode(img_file.read()).decode('utf-8')
                    
                result = is_human(image_path)
                if result == 0:
                    os.remove(image_path)
                    return apology("couldnt recognize human in picture", 404)
                
                elif result == 2:
                    os.remove(image_path)
                    return apology("provide a picture with only 1 face", 404)
                                    
                # Your API call or processing with the base64 string
                body = {
                    "user_id": id,
                    "pic": img_string
                }
                call_api("post_picture", body)

                # Return success or redirect as needed
                return redirect("/")
            else:
                return apology("Invalid file type. Please upload an image (png, jpg, jpeg)", 400)
        
        
        # Remember which user has logged in
        session["user_id"] = id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)