
from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtGui import QPalette, QColor, QIcon
from PyQt6.QtCore import Qt




class PageManagerWindow(QMainWindow):
    def __init__(self):
         
        super().__init__()
        self.pages = {}
        self.curent_userid = None
        self.setWindowTitle("Todo App")
        self.setWindowIcon(QIcon('images/checklist.png'))
        self.setFixedSize(450, 600)
 

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        

    def add_page(self, page_widget, page_name):
        self.pages[page_name] = page_widget
        self.stack.addWidget(page_widget)
    
    def set_current_user(self, userid):
        self.curent_userid = userid
    def get_current_user(self):
        return self.curent_userid
    
    def switch_page(self, page_name):
        if page_name in self.pages:
            widget = self.pages[page_name]
            self.stack.setCurrentWidget(widget)
        else:
            raise ValueError(f"Page '{page_name}' not found.")
    def get_page(self, page_name) :
        if page_name in self.pages:
            return self.pages[page_name]
        else:
            raise ValueError(f"Page '{page_name}' not found.")
    # def get_page(self, page_name: str):
    #     return self.pages.get(page_name)