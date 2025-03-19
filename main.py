from flask import Flask, request, render_template, redirect, url_for
import pytesseract 
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\ax_gi\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
from PIL import Image
import os
import uuid

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'uploads/'

def cleanfolder(folder, max_files=5):
    files = [os.path.join(folder, f) for f in os.listdir(folder)
             if os.path.isfile(os.path.join(folder, f))]

    if len(files) > max_files:
        files.sort(key=lambda x: os.path.getmtime(x))
        for i in range(len(files) - max_files):
            os.remove(files[i])

@app.route('/home', methods=['GET', 'POST'])

def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file in the request", 400
        
        file = request.files['file']
        if file.filename == '':
            return "No file selected", 400
        
        filename = f"{uuid.uuid4()}_{file.filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        cleanfolder(app.config['UPLOAD_FOLDER'], max_files=5)
        
        text = ocr_image(file_path)
        
        return render_template('results.html', text=text)
    
    return render_template('index.html')
    
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