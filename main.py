from flask import Flask, request, render_template, redirect, url_for
import pytesseract
from PIL import Image
import os
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file in the request", 400
        
        file = request.files['file']
        if file.filename == '':
            return "No file selected", 400
        
        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        text = ocr_image(file_path)
        
        return render_template('result.html', text=text)
    
def ocr_image(image_path):
    img = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(img)
    return extracted_text

@app.route('/about')
def about():
    return "test handwritting reader"

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)