# PIC-FINDER
#### Video Demo:  <https://youtu.be/IE3KVidzk88>
#### Description: My PIC-FINDER project is a web application designed to assist users in effortlessly locating themselves within a collection of pictures, especially those captured during events, parties, or social gatherings. Users begin by creating an account, providing a personalized experience for managing their images. Once logged in, they can upload a folder of pictures, and the application utilizes face recognition AI to identify the user's face within the images. After that, the recognized images can be downloaded as a zip folder to the users device. Additionally, the application features a clean and simple user interface, making the process seamless and enjoyable. 

## Features
#### **Face Recognition**: The application uses face recognition to identify your face in the uploaded pictures. You can upload a folder of pictures, and the application will determine if you are present in any of them.
#### **Users**: Each user has their unique account containing pictures of themselves that the AI uses to detect them in other photos

## Prerequisites

#### **Python (version 3.9)**
```
Package                 Version
----------------------- ----------
bcrypt                  4.1.1
bidict                  0.22.1
blinker                 1.7.0
cachelib                0.10.2
certifi                 2023.11.17
charset-normalizer      3.3.2
click                   8.1.7
cmake                   3.27.9
colorama                0.4.6
dlib                    19.24.2
face-recognition        1.3.0
face-recognition-models 0.3.0
Flask                   3.0.0
Flask-Session           0.5.0
Flask-SocketIO          5.3.6
h11                     0.14.0
idna                    3.6
importlib-metadata      7.0.0
itsdangerous            2.1.2
Jinja2                  3.1.2
MarkupSafe              2.1.3
numpy                   1.26.2
opencv-python           4.8.1.78
Pillow                  10.1.0
pip                     23.3.1
python-engineio         4.8.0
python-socketio         5.10.0
requests                2.31.0
setuptools              69.0.2
simple-websocket        1.0.0
urllib3                 2.1.0
Werkzeug                3.0.1
wheel                   0.42.0
wsproto                 1.2.0
zipp                    3.17.0
```

## Installation
#### To install and run the application, follow these steps:
1. ```virtualenv name```
2. ```name\Scripts\activate```
3. #### copy the code into virtual enviroment
4. #### install all packages
5. ```flask run```

## Usage
1. #### launch flask app
2. #### create an account
3. #### upload pictures of yourself (the more the better)
4. #### go to main page and upload pictures where you want to be found in


## Infrastructure
#### I have a "static" folder for "bootstrap.css" (sketch style) and user-uploaded pics in a sub-folder "uploads". The "templates" folder contains HTML files for how things look. In the main file - "app.py," all the routes and app logic is calculated. The helper file "helpers.py" brings in handy functions to keep the structure of "app.py" clean. Behind the scenes, data is stored in the 000webhost database, which comunicates with the wibsite by a PHP API. For face recognition I used the dlib model - face_recognition library.

## Disclaimer
#### The used AI model is not the best and might only recognize people who are directly facing the camera with their whole face fully visible
 
