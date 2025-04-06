
from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtGui import QPalette, QColor, QIcon
from PyQt6.QtCore import Qt




class PageManagerWindow(QMainWindow):
    def __init__(self):
         
        super().__init__()
        self.pages = {}

        self.setWindowTitle("Todo App")
        self.setWindowIcon(QIcon('images/checklist.png'))
        self.setFixedSize(450, 600)
        self.set_darkTheme()

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        

    def set_darkTheme(self):

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        self.setPalette(palette)


    def add_page(self, page_widget, page_name):
        self.pages[page_name] = page_widget
        self.stack.addWidget(page_widget)
    
    
    def switch_page(self, page_name):
        if page_name in self.pages:
            widget = self.pages[page_name]
            self.stack.setCurrentWidget(widget)
        else:
            raise ValueError(f"Page '{page_name}' not found.")
