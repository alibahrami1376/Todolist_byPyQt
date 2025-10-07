from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QAction

class CustomMenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        # ساخت منوهای اصلی
        file_menu = QMenu('فایل', self)
        edit_menu = QMenu('ویرایش', self)
        view_menu = QMenu('نمایش', self)
        help_menu = QMenu('راهنما', self)

        # افزودن گزینه‌ها به منوی فایل
        new_action = QAction('جدید', self)
        open_action = QAction('باز کردن', self)
        exit_action = QAction('خروج', self)
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # افزودن گزینه‌ها به منوی ویرایش
        undo_action = QAction('بازگردانی', self)
        redo_action = QAction('دوباره', self)
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

        # افزودن گزینه‌ها به منوی نمایش
        dark_mode_action = QAction('حالت دارک', self)
        view_menu.addAction(dark_mode_action)

        # افزودن گزینه‌ها به منوی راهنما
        about_action = QAction('درباره', self)
        help_menu.addAction(about_action)

        # افزودن منوها به نوار منو
        self.addMenu(file_menu)
        self.addMenu(edit_menu)
        self.addMenu(view_menu)
        self.addMenu(help_menu)
