from io import BytesIO
import openai
import json
import os
from flask import Flask, request, jsonify, render_template
from PyPDF2 import PdfReader
from flask_cors import CORS
import base64
from pdf2image import convert_from_path
import openai
# Set your OpenAI API key

openai.api_key =""


application = Flask(__name__)
CORS(application)
application.config['UPLOAD_FOLDER'] = 'uploads/'
pdfFile_path = "context.pdf"


@application.route('/', methods=['GET'])
def index():
   return render_template('index.html')

@application.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    print(pdfFile_path)
    content = read_pdf(pdfFile_path)
    if not content:
        return jsonify({"answer": "No content found in the file. Please upload your file"})
    
    data = jsonify({"answer": inquire_openai_api(question ,content)})
    # question is looked up in the file content
    return data

@application.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(message='No file part'), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify(message='No selected file'), 400

    if file:
        filename = file.filename
        file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
        global pdfFile_path
        pdfFile_path = application.config['UPLOAD_FOLDER'] + filename
        return jsonify(message='File successfully uploaded'), 200


def read_pdf(file_path):
    if not os.path.exists(file_path):
        return  None
    
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        content = ""
        for page in reader.pages:
            content += page.extract_text()
    return content

def read_image(file_path):
    with open(file_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    return encoded_image
def inquire_openai_api(question, file_content):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"The following is the content of a file: {file_content}\n\nBased on the above content, please answer the following question: {question}"}
        ]
    )
    return response.choices[0].message['content'].strip()


def analyze_pdf_images(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300)
    results = []

    for i, page in enumerate(pages):
        # Convert to base64
        buffer = BytesIO()
        page.save(buffer, format="JPEG")
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")

        # Send to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Vision model
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"Analyze page {i+1} of this document. What does it say or contain?"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded}", "detail": "auto"}}
                    ]
                }
            ]
        )
        results.append(response.choices[0].message['content'])
    print(results)
    return "\n\n".join(results)


if __name__ == "__main__":

    if not os.path.exists(application.config['UPLOAD_FOLDER']):
        os.makedirs(application.config['UPLOAD_FOLDER'])
    print(openai.__version__)
    application.run(host="0.0.0.0", 
            port=8080)