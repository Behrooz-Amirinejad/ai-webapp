import openai
import json
import os
from flask import Flask, request, jsonify, render_template
from PyPDF2 import PdfReader

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')# "sk-None-eYc8wX1bxZwlSVo6QlxjT3BlbkFJTY1wZHHOrRTaBBDw5g6k"


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
pdfFile_path = "context.pdf"


@app.route('/', methods=['GET'])
def index():
   return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    content = read_pdf(pdfFile_path)
    if not content:
        return jsonify({"answer": "No content found in the file. Please upload your file"})
    
    data = jsonify({"answer": inquire_openai_api(question ,content)})
    # question is looked up in the file content
    return data

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(message='No file part'), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify(message='No selected file'), 400

    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        global pdfFile_path
        pdfFile_path = app.config['UPLOAD_FOLDER'] + filename
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

def inquire_openai_api(question, file_content):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"The following is the content of a file: {file_content}\n\nBased on the above content, please answer the following question: {question}"}
        ]
    )
    return response.choices[0].message['content'].strip()


if __name__ == "__main__":

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    print(openai.__version__)
    app.run(host="0.0.0.0", 
            port=8080)