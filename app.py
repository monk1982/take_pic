from flask import Flask, render_template, Response, request, redirect, url_for
import cv2 as cv
import threading
import datetime
import os
import numpy as np
from PIL import Image

global switch, lb_button, capture, img_url

switch=0
capture=0
img_path = "static/captures"
lb_button = 'Bật Camera'
cur_frame = None
img_url=None
frame_lock = threading.Lock()

#make shots directory to save pics
try:
    os.mkdir(img_path)
except OSError as error:
    pass

#instatiate flask app  
app = Flask(__name__, template_folder='./templates')

def generate_frame():
    global cur_frame, capture
    cam = cv.VideoCapture(0)    
    while True:
        success, frame = cam.read()
        if not success:
            break
        with frame_lock:
            cur_frame = frame.copy()

        _, buffer = cv.imencode('.jpg',frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# Code hiển thị trình duyệt
@app.route('/')
def index():
    return render_template('index.html', lb_button=lb_button)

@app.route('/video_feed')
def video_feed():     
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def capture_image():
    global cur_frame
    with frame_lock:
        if cur_frame is not None:
            now = datetime.datetime.now()
            filename = os.path.sep.join([img_path, "capture_{}.png".format(str(now).replace(":",''))])
            fname =  'captures/'+"capture_{}.png".format(str(now).replace(":",''))
            cv.imwrite(filename, cur_frame)
            img_url=url_for('static', filename=fname)
    return img_url

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch, lb_button, capture,img_url
    if request.method == 'POST':
        if request.form.get('click') == 'Chụp Ảnh':                        
            img_url = capture_image()
            switch = 0   
            capture = 1         
            lb_button='Bật Camera'                                           
        else: 
            if (request.form.get('stop') == 'Bật Camera' ):                        
                switch = 1
                capture = 0
                lb_button='Tắt Camera'                               
            else:
                switch = 0
                capture = 0
                lb_button='Bật Camera'

    elif request.method=='GET':
        return render_template('index.html',lb_button=lb_button,capture=capture,img_url=img_url)
    
    return render_template('index.html',lb_button=lb_button,capture=capture,img_url=img_url)

# Code chạy lệnh Python
if __name__ == '__main__':
    app.run()
        