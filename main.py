from flask import Flask, request, render_template
import io
import PyPDF2

app = Flask(__name__)


def search_pdfs(files, keyword):
    results = []
    for file in files:
        file.seek(0)  # Reset file pointer to the beginning
        reader = PyPDF2.PdfReader(file)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if keyword.lower() in text.lower():
                results.append(f"Found '{keyword}' in {file.filename}, page {i + 1}")
    return results


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        keyword = request.form["keyword"]  # Get the search keyword from the form

        uploaded_files = request.files.getlist("pdf_file")  # Get the uploaded files
        if uploaded_files:
            # In-memory processing without saving to disk
            files = [file.stream for file in uploaded_files]  # In-memory file object (stream)

            # Search through the uploaded files
            results = search_pdfs(files, keyword)
        else:
            results.append("No files uploaded.")

    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)