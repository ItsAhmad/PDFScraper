import os
import fitz  # PyMuPDF
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QTextBrowser, QPushButton, QFileDialog, \
    QLineEdit, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl


class PDFSearcherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Searcher")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        layout = QVBoxLayout()

        self.folder_label = QLabel("Selected Folder:")
        self.keyword_input = QLineEdit(self)
        self.keyword_input.setPlaceholderText("Enter keyword...")
        self.results_area = QTextBrowser(self)  # Use QTextBrowser for clickable links
        self.results_area.setOpenExternalLinks(False)  # Disable default link behavior
        self.results_area.anchorClicked.connect(self.open_pdf)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.browse_and_search)

        layout.addWidget(self.folder_label)
        layout.addWidget(self.keyword_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.results_area)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def browse_and_search(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_label.setText(f"Selected Folder: {folder}")
            keyword = self.keyword_input.text()
            if keyword:
                # Reset results area at the start of a new search
                self.results_area.clear()
                self.results_area.append(f"<b>Searching in folder:</b> {folder}<br><br>")
                QApplication.processEvents()  # Allow UI updates during processing

                # Perform the search
                results = self.perform_search(folder, keyword)

                # Display results after search completes
                if results:
                    self.results_area.append("<b>Search Results:</b><br><br>")
                    self.results_area.append("\n".join(results))
                else:
                    self.results_area.append("<b>No matches found.</b>")

    def perform_search(self, directory, keyword):
        results = []
        for file in os.listdir(directory):
            if file.endswith('.pdf'):
                path = os.path.join(directory, file)

                # Add plain text status update (not clickable)
                self.results_area.append(f"<span style='color: gray;'>Searching in {file}...</span>")
                QApplication.processEvents()  # Allow UI updates during processing

                try:
                    doc = fitz.open(path)  # Open the PDF
                    for i, page in enumerate(doc):
                        text = page.get_text()
                        if keyword.lower() in text.lower():
                            # Create clickable link for results
                            results.append(f'<a href="file://{os.path.abspath(path)}">{file}, page {i + 1}</a><br><br>')
                    doc.close()
                except Exception as e:
                    results.append(f"Error processing {file}: {e}")
        return results

    def open_pdf(self, url):
        # Open the PDF file using the system's default viewer
        QDesktopServices.openUrl(QUrl.fromLocalFile(url.toLocalFile()))
        # Prevent QTextBrowser from navigating or changing content
        self.results_area.setSource(QUrl())  # Clears navigation trigger


if __name__ == "__main__":
    app = QApplication([])
    window = PDFSearcherApp()
    window.show()
    app.exec()
