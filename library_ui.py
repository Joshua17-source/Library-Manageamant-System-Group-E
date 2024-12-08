from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QPushButton, QTabWidget,
    QLabel, QFrame, QMessageBox, QSpacerItem, QSizePolicy, QTableWidget, QTableWidgetItem, QHeaderView,
    QDialog, QFileDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDateTime, QTimer
import csv
import logging
from database_manager import DatabaseManager

# Configure logging for error handling
logging.basicConfig(filename='app.log', level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.authenticate)

        layout.addWidget(QLabel("Enter your credentials:"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def authenticate(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        if username == "Joshua" and password == "16474":
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")


class LibraryApp(QWidget):
    def __init__(self):
        super().__init__()
        login_dialog = LoginDialog()
        if login_dialog.exec_() == QDialog.Accepted:
            self.db = DatabaseManager()
            self.init_ui()
        else:
            self.close()

    def init_ui(self):
        self.setWindowTitle("Library Management System")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background-color: #d1f0f1; color: #333; font-family: Arial; font-size: 14px;")

        main_layout = QVBoxLayout(self)

        # Add date and time display with continuous update
        self.datetime_label = QLabel()
        self.datetime_label.setAlignment(Qt.AlignRight)
        self.datetime_label.setStyleSheet("font-size: 12px; color: #444; padding: 5px;")
        main_layout.addWidget(self.datetime_label)

        timer = QTimer(self)
        timer.timeout.connect(self.update_datetime)
        timer.start(1000)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""QTabWidget::pane { border: 1px solid #4a89dc; }
            QTabBar::tab { background-color: #4a89dc; color: white; padding: 10px; margin-right: 5px; border-radius: 3px; }
            QTabBar::tab:selected { background-color: #357ebd; }
            QTabBar::tab:hover { background-color: #2e6da4; }
        """)
        main_layout.addWidget(self.tabs)

        self.manage_books_tab = QWidget()
        self.about_tab = QWidget()

        self.tabs.addTab(self.manage_books_tab, "Manage Books")
        self.tabs.addTab(self.about_tab, "About")

        self.setup_manage_books_tab()
        self.setup_about_tab()

        # Add theme toggle button
        self.theme_button = QPushButton("Toggle Dark Mode")
        self.theme_button.clicked.connect(self.toggle_theme)
        main_layout.addWidget(self.theme_button)

        self.setLayout(main_layout)

    def update_datetime(self):
        current_datetime = QDateTime.currentDateTime().toString("dddd, MMMM d, yyyy hh:mm:ss ap")
        self.datetime_label.setText(current_datetime)

    def setup_manage_books_tab(self):
        layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_button = QPushButton("Search")
        self.clear_search_button = QPushButton("Clear")

        self.search_input.setFixedWidth(300)
        self.search_button.setFixedWidth(120)
        self.clear_search_button.setFixedWidth(120)

        self.search_input.setStyleSheet(
            "background-color: #ffffff; color: #444; padding: 8px; border-radius: 5px; border: 1px solid #dcdcdc;")
        self.search_button.setStyleSheet(self.get_button_style())
        self.clear_search_button.setStyleSheet(self.get_button_style())

        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        search_layout.addWidget(self.clear_search_button)
        layout.addLayout(search_layout)

        form_frame = QFrame()
        form_frame.setStyleSheet(
            "background-color: #ececec; border-radius: 10px; border: 1px solid #dcdcdc; padding: 20px;")
        form_layout = QFormLayout(form_frame)

        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.isbn_input = QLineEdit()
        self.genre_input = QLineEdit()
        self.year_input = QLineEdit()

        input_style = "background-color: #ffffff; color: #333; padding: 8px; border-radius: 5px; border: 1px solid #ccc;"

        self.title_input.setStyleSheet(input_style)
        self.author_input.setStyleSheet(input_style)
        self.isbn_input.setStyleSheet(input_style)
        self.genre_input.setStyleSheet(input_style)
        self.year_input.setStyleSheet(input_style)

        form_layout.addRow("Title:", self.title_input)
        form_layout.addRow("Author:", self.author_input)
        form_layout.addRow("ISBN:", self.isbn_input)
        form_layout.addRow("Genre:", self.genre_input)
        form_layout.addRow("Year:", self.year_input)

        layout.addWidget(form_frame)

        button_layout = QHBoxLayout()
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.add_button = QPushButton("Add Book")
        self.update_button = QPushButton("Update Book")
        self.delete_button = QPushButton("Delete Book")
        self.clear_form_button = QPushButton("Clear Form")
        self.export_button = QPushButton("Export to CSV")

        self.add_button.setStyleSheet(self.get_button_style())
        self.update_button.setStyleSheet(self.get_button_style())
        self.delete_button.setStyleSheet(self.get_button_style())
        self.clear_form_button.setStyleSheet(self.get_button_style())
        self.export_button.setStyleSheet(self.get_button_style())

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_form_button)
        button_layout.addWidget(self.export_button)
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        layout.addLayout(button_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Author", "ISBN", "Genre", "Year"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setStyleSheet("""
            QTableWidget { background-color: #ffffff; color: #333; }
            QHeaderView::section { background-color: #4a89dc; color: white; padding: 5px; }
        """)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setStretchLastSection(True)

        layout.addWidget(self.table)
        self.manage_books_tab.setLayout(layout)

        self.add_button.clicked.connect(self.add_book)
        self.update_button.clicked.connect(self.update_book)
        self.delete_button.clicked.connect(self.delete_book)
        self.search_button.clicked.connect(self.search_books)
        self.clear_search_button.clicked.connect(self.clear_search)
        self.clear_form_button.clicked.connect(self.clear_form)
        self.export_button.clicked.connect(self.export_to_csv)

        self.update_table()
        self.table.selectionModel().selectionChanged.connect(self.populate_form_from_table)

    def get_button_style(self):
        return """
            QPushButton { 
                background-color: #5bc0de; color: white; padding: 10px 15px; border-radius: 5px; 
                font-weight: bold; font-size: 14px; margin: 5px;
            }
            QPushButton:hover {
                background-color: #31b0d5;
            }
        """

    def add_book(self):
        try:
            self.validate_form()
            title = self.title_input.text().strip()
            author = self.author_input.text().strip()
            isbn = self.isbn_input.text().strip()
            genre = self.genre_input.text().strip()
            year = self.year_input.text().strip()

            self.db.add_book(title, author, isbn, genre, year)
            self.show_message("Success", "Book added successfully.")
            self.clear_form()
            self.update_table()
        except ValueError as e:
            self.show_message("Error", str(e))

    def update_book(self):
        try:
            self.validate_form()
            selected_row = self.table.currentRow()
            if selected_row < 0:
                raise ValueError("Please select a book to update.")

            book_id = int(self.table.item(selected_row, 0).text())
            title = self.title_input.text().strip()
            author = self.author_input.text().strip()
            isbn = self.isbn_input.text().strip()
            genre = self.genre_input.text().strip()
            year = self.year_input.text().strip()

            self.db.update_book(book_id, title, author, isbn, genre, year)
            self.show_message("Success", "Book updated successfully.")
            self.clear_form()
            self.update_table()
        except ValueError as e:
            self.show_message("Error", str(e))

    def delete_book(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            self.show_message("Error", "Please select a book to delete.")
            return

        book_id = int(self.table.item(selected_row, 0).text())
        self.db.delete_book(book_id)
        self.show_message("Success", "Book deleted successfully.")
        self.clear_form()
        self.update_table()

    def search_books(self):
        """
        Searches for books and updates the table with the results.
        """
        try:
            search_term = self.search_input.text().strip()
            if not search_term:
                self.show_message("Input Error", "Please enter a search term.")
                return

            # Fetch results from the database
            results = self.db.search_books(search_term)

            if results:
                self.update_table(results)
            else:
                self.show_message("No Results", f"No books found for '{search_term}'.")
        except Exception as e:
            logging.exception("Unexpected error during search operation.")
            self.show_message("Error", f"An error occurred while searching: {e}")

    def clear_search(self):
        self.search_input.clear()
        self.update_table()

    def clear_form(self):
        self.title_input.clear()
        self.author_input.clear()
        self.isbn_input.clear()
        self.genre_input.clear()
        self.year_input.clear()

    def validate_form(self):
        if not self.title_input.text().strip():
            raise ValueError("Title is required.")
        if not self.author_input.text().strip():
            raise ValueError("Author is required.")
        if not self.isbn_input.text().strip().isdigit():
            raise ValueError("ISBN must be numeric.")
        if not self.genre_input.text().strip():
            raise ValueError("Genre is required.")
        if not self.year_input.text().strip().isdigit() or len(self.year_input.text().strip()) != 4:
            raise ValueError("Year must be a valid 4-digit number.")

    def update_table(self, books=None):
        """
        Update the table with the provided books or fetch all books.
        """
        try:
            # Get all books if none are provided
            if books is None:
                books = self.db.get_books()

            # Clear the table and populate rows
            self.table.setRowCount(0)
            for book in books:
                row_index = self.table.rowCount()
                self.table.insertRow(row_index)
                for col_index, value in enumerate(book):
                    self.table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

        except Exception as e:
            logging.exception("Failed to update the table.")
            self.show_message("Error", "An unexpected error occurred while updating the table.")

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID column
        header.setSectionResizeMode(1, QHeaderView.Stretch)          # Title column
        header.setSectionResizeMode(2, QHeaderView.Stretch)          # Author column
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents) # ISBN column
        header.setSectionResizeMode(4, QHeaderView.Stretch)          # Genre column
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents) # Year column

    def populate_form_from_table(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            return

        self.title_input.setText(self.table.item(selected_row, 1).text())
        self.author_input.setText(self.table.item(selected_row, 2).text())
        self.isbn_input.setText(self.table.item(selected_row, 3).text())
        self.genre_input.setText(self.table.item(selected_row, 4).text())
        self.year_input.setText(self.table.item(selected_row, 5).text())

    def export_to_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export to CSV", "", "CSV files (*.csv)")
        if path:
            try:
                books = self.db.get_books()
                with open(path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(["ID", "Title", "Author", "ISBN", "Genre", "Year"])
                    writer.writerows(books)
                self.show_message("Success", "Data exported successfully.")
            except Exception as e:
                self.show_message("Error", f"Failed to export data: {str(e)}")

    def toggle_theme(self):
        dark_style = """
            QWidget { background-color: #2e2e2e; color: #E0E0E0; }  /* Light Gray text */
            QLabel { color: #F5A623; }  /* Warm Yellow for date label */
            QLineEdit { background-color: #393939; color: #FFFFFF; border: 1px solid #555555; }
            QTableWidget { background-color: #393939; color: #FFFFFF; }
            QHeaderView::section { background-color: #3B3B3B; color: #E0E0E0; }
            QPushButton { background-color: #5a5a5a; color: white; }
            QPushButton:hover { background-color: #6c6c6c; }
        """
        light_style = """
            QWidget { background-color: #FFFFFF; color: #333333; }  /* Dark Gray text */
            QLabel { color: #444444; }  /* Muted Gray for date label */
            QLineEdit { background-color: #FFFFFF; color: #000000; border: 1px solid #CCCCCC; }
            QTableWidget { background-color: #FFFFFF; color: #000000; }
            QHeaderView::section { background-color: #4A89DC; color: #FFFFFF; }
            QPushButton { background-color: #5BC0DE; color: white; }
            QPushButton:hover { background-color: #31B0D5; }
        """
        current_style = self.styleSheet()
        if current_style == dark_style:
            self.setStyleSheet(light_style)  # Switch to light mode
            self.datetime_label.setStyleSheet(
                "font-size: 12px; color: #444444; padding: 5px;")  # Muted Gray for light mode
        else:
            self.setStyleSheet(dark_style)  # Switch to dark mode
            self.datetime_label.setStyleSheet(
                "font-size: 12px; color: #F5A623; padding: 5px;")  # Warm Yellow for dark mode

    def setup_about_tab(self):
        layout = QVBoxLayout()
        about_label = QLabel("<h2>Library Management System</h2><p>Version: 1.0</p><p>Joshua Osangie Kamara</p><p> Abraham Bobson Turay</p><p>Nenneh Kallay</p><p>Mariama M. Kanu</p><p>James</p><p>Emelda Jestina Margai</p>")
        about_label.setAlignment(Qt.AlignCenter)  # Center-align the text
        about_label.setObjectName("about_label")
        layout.addWidget(about_label)
        self.about_tab.setLayout(layout)

    def show_message(self, title, message):
        QMessageBox.information(self, title, message)
