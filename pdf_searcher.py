import os
import fitz  # PyMuPDF
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel,
    QLineEdit, QTextEdit, QFileDialog, QHBoxLayout
)
from PyQt5.QtCore import Qt


class PDFSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Search Tool")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Directory selection
        dir_layout = QHBoxLayout()
        self.dir_label = QLabel("Select Folder:")
        self.dir_input = QLineEdit()
        self.dir_input.setPlaceholderText("Choose a folder...")
        self.dir_input.setReadOnly(True)
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_directory)

        dir_layout.addWidget(self.dir_label)
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(self.browse_button)
        layout.addLayout(dir_layout)

        # Keyword input
        self.keyword_label = QLabel("Keyword:")
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("Enter keyword to search")
        layout.addWidget(self.keyword_label)
        layout.addWidget(self.keyword_input)

        # Results area
        self.results_area = QTextEdit()
        self.results_area.setReadOnly(True)
        layout.addWidget(self.results_area)

        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.start_search)
        layout.addWidget(self.search_button)

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Folder")
        if directory:
            self.dir_input.setText(directory)

    def start_search(self):
        # Clear previous results
        self.results_area.clear()

        # Get user inputs
        directory = self.dir_input.text()
        keyword = self.keyword_input.text()

        if not directory:
            self.results_area.append("Error: No folder selected.\n")
            return
        if not keyword:
            self.results_area.append("Error: No keyword entered.\n")
            return

        # Perform search
        results = self.perform_search(directory, keyword)

        # Display results
        self.results_area.append("\nSearch Complete! Results:\n")
        if results:
            self.results_area.append("\n\n".join(results))
        else:
            self.results_area.append("No matches found.")

    def perform_search(self, directory, keyword):
        results = []
        batch = []  # To collect updates in batches
        batch_size = 5  # Number of files to process before updating the UI

        files = [file for file in os.listdir(directory) if file.endswith('.pdf')]
        total_files = len(files)

        for idx, file in enumerate(files, start=1):
            path = os.path.join(directory, file)
            batch.append(f"Searching in {file}...")

            try:
                with fitz.open(path) as pdf_file:
                    for i, page in enumerate(pdf_file):
                        text = page.get_text()
                        if keyword.lower() in text.lower():
                            results.append(f"Found '{keyword}' in {file}, page {i + 1}")
            except Exception as e:
                results.append(f"Error processing {file}: {e}")

            # Update UI after processing each batch of files
            if idx % batch_size == 0 or idx == total_files:
                self.results_area.append("\n".join(batch))
                batch.clear()  # Clear the batch after updating the UI
                QApplication.processEvents()  # Allow UI to update

        return results


if __name__ == "__main__":
    app = QApplication([])
    window = PDFSearchApp()
    window.show()
    app.exec()
