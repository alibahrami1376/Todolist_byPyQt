from PyQt6.QtWidgets import QFrame, QVBoxLayout, QToolButton, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QIcon

VS_PALETTE = {
    "bg": "#1b1f2b",
    "bg_light": "#23283a",
    "text": "#d7dae0",
    "accent": "#569cd6",
    "hover": "rgba(255, 255, 255, 0.06)",
}


class Sidebar(QFrame):
    switch_requested = pyqtSignal(str)
    request_hide = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.expanded = True
        self.is_dark = True
        self.setFixedWidth(120)
        self.setObjectName("sidebar-frame")
        self.setStyleSheet(
            """
            QFrame#sidebar-frame {
                background-color: #1b1f2b;
                border-right: 1px solid #262b3c;
            }
        """
        )

        self.layout_main = QVBoxLayout(self)
        self.layout_main.setContentsMargins(8, 16, 8, 16)
        self.layout_main.setSpacing(18)
        self.buttons = {}

        # Toggle (collapse/expand) button at the top
        self.toggle_button = QToolButton()
        self.toggle_button.setIcon(QIcon("icons/more.png"))
        self.toggle_button.setIconSize(QSize(20, 20))
        self.toggle_button.setToolTip("Collapse/Expand")
        self.toggle_button.setCheckable(False)
        self.toggle_button.clicked.connect(self.toggle)
        self.layout_main.addWidget(self.toggle_button)

        self.sections = [
            ("Dashboard", "dashboard.png"),
            ("Projects", "task.png"),
            ("Checklist", "task.png"),  # چک‌لیست عادت‌ها
            ("MoreFeatures", "more.png"), 
            ("Ideas", "add.png"),
            ("Login", "login.png"),
            ("Settings", "settings.png"),
            ("About", "about.png"),
        ]

        for name, icon in self.sections:
            self.add_button(name, icon)

        self.layout_main.addStretch()

        # Now that buttons exist, apply full theme
        self.apply_theme(self.is_dark)

    def add_button(self, name, icon_file):
        btn = QToolButton()
        btn.setText(name if self.expanded else "")
        btn.setIcon(QIcon(f"icons/{icon_file}"))
        btn.setIconSize(QSize(24, 24))
        btn.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextUnderIcon
            if self.expanded
            else Qt.ToolButtonStyle.ToolButtonIconOnly
        )
        btn.setObjectName(name.lower())
        btn.setCheckable(True)
        btn.setStyleSheet(self.style_button(False, self.is_dark))
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn.clicked.connect(lambda checked, n=name: self.on_click(n))
        self.layout_main.addWidget(btn)
        self.buttons[name] = btn

    def on_click(self, name):
        for btn_name, btn in self.buttons.items():
            btn.setChecked(btn_name == name)
            btn.setStyleSheet(self.style_button(btn.isChecked(), self.is_dark))
        self.switch_requested.emit(name.lower())

    def style_button(self, active, is_dark):
        text_color = VS_PALETTE["text"] if is_dark else "#1f1f1f"
        base_bg = VS_PALETTE["bg"] if is_dark else "#f4f4f4"
        hover_bg = VS_PALETTE["hover"] if is_dark else "#e9e9e9"
        accent = VS_PALETTE["accent"]

        if active:
            return f"""
                QToolButton {{
                    text-align: left;
                    padding-left: 12px;
                    padding-right: 8px;
                    color: {accent};
                    background-color: rgba(86, 156, 214, 0.18);
                    border-left: 4px solid {accent};
                    border-radius: 12px;
                    font-weight: 600;
                }}
                QToolButton:hover {{
                    background-color: rgba(86, 156, 214, 0.28);
                }}
            """
        return f"""
            QToolButton {{
                text-align: left;
                padding-left: 12px;
                padding-right: 8px;
                color: {text_color};
                background-color: {base_bg};
                border: none;
                border-radius: 12px;
            }}
            QToolButton:hover {{
                background-color: {hover_bg};
            }}
        """

    def toggle(self):
        self.expanded = not self.expanded
        if not self.expanded:
            # درخواست برای مخفی شدن کامل سایدبار
            self.request_hide.emit()
            return
        # بازگردانی حالت باز
        self.setFixedWidth(120)
        for name, btn in self.buttons.items():
            btn.setText(name)
            btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            btn.setStyleSheet(self.style_button(btn.isChecked(), self.is_dark))
        self.apply_theme(self.is_dark)

    def apply_theme(self, is_dark: bool):
        self.is_dark = is_dark
        if is_dark:
            self.setStyleSheet(
                """
                QFrame#sidebar-frame {
                    background-color: #1b1f2b;
                    border-right: 1px solid #262b3c;
                }
            """
            )
        else:
            self.setStyleSheet(
                "QFrame#sidebar-frame { background-color: #f1f1f1; border-right: 1px solid #e0e0e0; }"
            )
        if not hasattr(self, "buttons"):
            return
        # style toggle button
        if hasattr(self, "toggle_button"):
            if is_dark:
                self.toggle_button.setStyleSheet(
                    f"""
                    QToolButton {{
                        background-color: transparent;
                        border: none;
                        color: {VS_PALETTE["text"]};
                    }}
                    QToolButton:hover {{
                        background-color: {VS_PALETTE["hover"]};
                        border-radius: 12px;
                    }}
                """
                )
            else:
                self.toggle_button.setStyleSheet(
                    "QToolButton { background-color: transparent; border: none; color: #1e1e1e; } QToolButton:hover { background-color: #e9e9e9; border-radius: 6px; }"
                )
        for name, btn in self.buttons.items():
            btn.setStyleSheet(self.style_button(btn.isChecked(), self.is_dark))
