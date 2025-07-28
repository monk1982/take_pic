from flask import Flask, render_template, Response, request, url_for
import base64
import cv2
import numpy as np

app = Flask(__name__, template_folder='./templates')

# Code hiển thị trình duyệt
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    data = request.get_json()
    image_b64 = data['image'].split(',')[1]  # bỏ phần đầu 'data:image/jpeg;base64,...'

    # Decode ảnh từ base64
    image_bytes = base64.b64decode(image_b64)
    np_arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Lưu ảnh
    cv2.imwrite('static/captures/uploaded.jpg', img)
    print("✅ Đã nhận và lưu ảnh từ client")

    return "Ảnh đã được gửi lên server!"

if __name__ == '__main__':
    app.run()