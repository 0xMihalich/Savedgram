from PyQt5.QtWidgets import QApplication

from savedgram import Savedgram

if __name__ == "__main__":
    import sys
 
    app = QApplication(sys.argv)
    main = Savedgram()
    main.show()
    sys.exit(app.exec())
