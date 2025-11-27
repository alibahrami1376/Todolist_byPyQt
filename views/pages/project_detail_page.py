from typing import Optional
from PyQt6.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QScrollArea,
    QFrame,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QSpinBox,
    QFormLayout,
    QMessageBox,
    QDialogButtonBox,
)
from PyQt6.QtCore import Qt
from services.project_service import ProjectService
from models.db.project_entity import ProjectEntity
from datetime import datetime
import os


class ProjectDetailPage(QDialog):
    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        self.project_service = ProjectService()
        self.project: ProjectEntity = None
        self.status_options = [
            ("Backlog", "todo"),
            ("In Progress", "doing"),
            ("Done", "done"),
        ]
        self.status_lookup = {value: label for label, value in self.status_options}
        self.edit_mode = False
        self.setWindowTitle("Project Details")
        self.setMinimumSize(600, 500)
        self.setWindowFlag(Qt.WindowType.WindowMinMaxButtonsHint, True)
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, True)


        self.init_ui()
        self.load_project_data()
        self.apply_theme()
        self.set_edit_mode(False)

    def get_current_theme(self):
        """Get current theme from config"""
        config_path = "configg/theme_config.txt"
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    theme = (f.read().strip() or "Dark").lower()
                    legacy_dark_values = {"dark", "\u062f\u0627\u0631\u06a9"}
                    return theme in legacy_dark_values
            except Exception:
                return True  # Default to dark
        return True  # Default to dark

    def apply_theme(self):
        """Apply theme based on current config"""
        is_dark = self.get_current_theme()
        if is_dark:
            self.setStyleSheet("""
                QWidget {
                    background-color: #1e1e1e;
                    color: white;
                    font-family: Segoe UI;
                    font-size: 14px;
                }
                QLabel {
                    color: white;
                }
                QPushButton {
                    background-color: #3e3e42;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #505050;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #ffffff;
                    color: #1e1e1e;
                    font-family: Segoe UI;
                    font-size: 14px;
                }
                QLabel {
                    color: #1e1e1e;
                }
                QPushButton {
                    background-color: #e6eaf3;
                    color: #1e1e1e;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #dfe7f7;
                }
            """)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)

        header = QHBoxLayout()
        back_btn = QPushButton("Close")
        back_btn.clicked.connect(self.close)
        header.addWidget(back_btn)
        header.addStretch()
        main_layout.addLayout(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(16)

        self.title_display = QLabel()
        self.title_display.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 6px;")
        self.title_display.setWordWrap(True)
        content_layout.addWidget(self.title_display)

        self.description_display = QLabel()
        self.description_display.setWordWrap(True)
        self.description_display.setStyleSheet("margin-bottom: 12px;")
        content_layout.addWidget(self.description_display)

        info_display_frame = QFrame()
        info_display_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.04);
                border-radius: 8px;
                padding: 12px;
            }
        """)
        info_display_layout = QFormLayout(info_display_frame)
        info_display_layout.setSpacing(10)

        self.status_display = QLabel()
        info_display_layout.addRow("Status:", self.status_display)

        self.progress_display = QLabel()
        info_display_layout.addRow("Progress:", self.progress_display)

        self.tech_stack_display = QLabel()
        info_display_layout.addRow("Tech stack:", self.tech_stack_display)

        self.start_date_display = QLabel()
        info_display_layout.addRow("Start date:", self.start_date_display)

        self.end_date_display = QLabel()
        info_display_layout.addRow("End date:", self.end_date_display)

        self.created_label = QLabel()
        info_display_layout.addRow("Created at:", self.created_label)

        content_layout.addWidget(info_display_frame)

        self.edit_form_frame = QFrame()
        self.edit_form_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 8px;
                padding: 12px;
            }
        """)
        edit_frame_layout = QVBoxLayout(self.edit_form_frame)
        edit_frame_layout.setContentsMargins(0, 0, 0, 0)
        edit_frame_layout.setSpacing(12)

        info_layout = QFormLayout()
        info_layout.setSpacing(12)

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Project title")
        info_layout.addRow("Title:", self.title_edit)

        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("Describe scope, goals, and deliverables")
        self.description_edit.setMinimumHeight(100)
        info_layout.addRow("Description:", self.description_edit)

        self.status_combo = QComboBox()
        for label, value in self.status_options:
            self.status_combo.addItem(label, value)
        info_layout.addRow("Status:", self.status_combo)

        self.progress_spin = QSpinBox()
        self.progress_spin.setRange(0, 100)
        self.progress_spin.setSuffix(" %")
        self.tech_stack_edit = QLineEdit()
        self.tech_stack_edit.setPlaceholderText("React, FastAPI, ...")
        info_layout.addRow("Progress:", self.progress_spin)
        info_layout.addRow("Tech stack:", self.tech_stack_edit)

        self.start_date_edit = QLineEdit()
        self.start_date_edit.setPlaceholderText("YYYY-MM-DD")
        info_layout.addRow("Start date:", self.start_date_edit)

        self.end_date_edit = QLineEdit()
        self.end_date_edit.setPlaceholderText("YYYY-MM-DD")
        info_layout.addRow("End date:", self.end_date_edit)

        edit_frame_layout.addLayout(info_layout)

        self.save_button = QPushButton("Save project changes")
        self.save_button.clicked.connect(self.save_project_changes)
        edit_frame_layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.edit_form_frame.setVisible(False)
        content_layout.addWidget(self.edit_form_frame)

        self.toggle_edit_button = QPushButton("Enable editing")
        self.toggle_edit_button.clicked.connect(self.toggle_edit_mode)
        content_layout.addWidget(self.toggle_edit_button)

        content_layout.addStretch()

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def load_project_data(self):
        self.project = self.project_service.get(self.project_id)
        if not self.project:
            self.title_display.setText("Project not found")
            return

        # Project title
        self.title_display.setText(f"<b>{self.project.title}</b>")
        self.title_edit.setText(self.project.title)

        # Description text
        description = self.project.description or self.project.summary or ""
        self.description_display.setText(f"<b>Description:</b><br>{description or '---'}")
        self.description_edit.setPlainText(description)

        # Status labels
        status_value = self.project.status or "todo"
        status_text = next((label for label, value in self.status_options if value == status_value), status_value)
        self.status_display.setText(status_text)
        idx = self.status_combo.findData(status_value)
        if idx >= 0:
            self.status_combo.setCurrentIndex(idx)

        # Progress display
        progress = self.project.progress or 0
        self.progress_display.setText(f"{progress}%")
        self.progress_spin.setValue(progress)

        # Tech stack display
        tech_text = self.project.tech_stack or "Not specified"
        self.tech_stack_display.setText(tech_text)
        self.tech_stack_edit.setText(self.project.tech_stack or "")

        # Date labels
        start_text = self.format_date(self.project.start_date) or "Not set"
        end_text = self.format_date(self.project.end_date) or "Not set"
        self.start_date_display.setText(start_text)
        self.end_date_display.setText(end_text)
        self.start_date_edit.setText(self.format_date(self.project.start_date))
        self.end_date_edit.setText(self.format_date(self.project.end_date))

        # Created timestamp
        created_str = "-"
        if self.project.created_at:
            created_str = self.project.created_at.strftime("%Y-%m-%d %H:%M")
        self.created_label.setText(created_str)


    def save_project_changes(self):
        title = self.title_edit.text().strip()
        if not title:
            QMessageBox.warning(self, "Missing title", "Project title is required.")
            return

        description = self.description_edit.toPlainText().strip()
        tech_stack = self.tech_stack_edit.text().strip()
        status = self.status_combo.currentData()
        progress = self.progress_spin.value()
        start_date = self.parse_date(self.start_date_edit.text().strip())
        end_date = self.parse_date(self.end_date_edit.text().strip())

        if self.start_date_edit.text().strip() and not start_date:
            QMessageBox.warning(self, "Invalid date", "Start date must follow YYYY-MM-DD.")
            return
        if self.end_date_edit.text().strip() and not end_date:
            QMessageBox.warning(self, "Invalid date", "End date must follow YYYY-MM-DD.")
            return

        payload = {
            "title": title,
            "description": description,
            "summary": description,
            "tech_stack": tech_stack,
            "status": status,
            "progress": progress,
            "start_date": start_date,
            "end_date": end_date,
        }

        updated = self.project_service.update(self.project_id, payload)
        if updated:
            QMessageBox.information(self, "Saved", "Project changes were saved successfully.")
            self.load_project_data()
        else:
            QMessageBox.warning(self, "Error", "Saving changes failed.")

    def format_date(self, value) -> str:
        if not value:
            return ""
        if isinstance(value, str):
            return value
        try:
            return value.strftime("%Y-%m-%d")
        except Exception:
            return ""

    def parse_date(self, value: str):
        if not value:
            return None
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return None

    def set_edit_mode(self, enabled: bool):
        self.edit_mode = enabled
        widgets = [
            self.title_edit,
            self.description_edit,
            self.status_combo,
            self.progress_spin,
            self.tech_stack_edit,
            self.start_date_edit,
            self.end_date_edit,
        ]
        for widget in widgets:
            widget.setEnabled(enabled)
        self.edit_form_frame.setVisible(enabled)
        self.save_button.setVisible(enabled)
        self.toggle_edit_button.setText("Cancel editing" if enabled else "Enable editing")

    def toggle_edit_mode(self):
        self.set_edit_mode(not self.edit_mode)


