import sys
from PyQt5.QtWidgets import QApplication
from library_ui import LibraryApp

def main():
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
