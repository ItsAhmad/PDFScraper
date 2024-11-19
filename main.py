from flask import Flask, request, render_template
import PyPDF2

app = Flask(__name__)


def search_pdfs(files_with_names, keyword):
    results = []
    for file_stream, filename in files_with_names:
        file_stream.seek(0)  # Reset the file pointer to the beginning
        reader = PyPDF2.PdfReader(file_stream)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if keyword.lower() in text.lower():
                results.append(f"Found '{keyword}' in {filename}, page {i + 1}")
    return results


@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        keyword = request.form["keyword"]  # Get the search keyword from the form

        uploaded_files = request.files.getlist("pdf_file")  # Get the uploaded files
        if uploaded_files:
            # Create a list of tuples containing file streams and their filenames
            files_with_names = [(file.stream, file.filename) for file in uploaded_files]

            # Search through the uploaded files
            results = search_pdfs(files_with_names, keyword)
        else:
            results.append("No files uploaded.")

    return render_template("index.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)