from flask import Flask, request, render_template
import os
import PyPDF2

app = Flask(__name__)

def search_pdfs(directory, keyword):
    results = []
    for file in os.listdir(directory):
        if file.endswith('.pdf'):
            path = os.path.join(directory, file)
            with open(path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                for i, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if keyword.lower() in text.lower():
                        results.append(f"Found '{keyword}' in {file}, page {i + 1}")
    return results

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        folder = request.form["folder"]
        keyword = request.form["keyword"]
        results = search_pdfs(folder, keyword)
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)