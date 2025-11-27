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
from services.project_step_service import ProjectStepService
from models.db.project_entity import ProjectEntity
from datetime import datetime
from functools import partial
import os


class ProjectDetailPage(QDialog):
    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        self.project_service = ProjectService()
        self.step_service = ProjectStepService()
        self.project: ProjectEntity = None
        self.steps_data = []
        self.status_options = [
            ("در انتظار", "todo"),
            ("در حال انجام", "doing"),
            ("انجام شده", "done"),
        ]
        self.board_statuses = [
            ("To Do", "todo"),
            ("Doing", "doing"),
            ("Done", "done"),
        ]
        self.edit_mode = False
        self.setWindowTitle("جزئیات پروژه")
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
                    theme = f.read().strip() or "روشن"
                    return theme == "دارک"
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

        # Header با دکمه بستن
        header = QHBoxLayout()
        back_btn = QPushButton("بستن")
        back_btn.clicked.connect(self.close)
        header.addWidget(back_btn)
        header.addStretch()
        main_layout.addLayout(header)

        # Scroll area برای محتوا
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(16)

        # عنوان پروژه
        self.title_display = QLabel()
        self.title_display.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 6px;")
        self.title_display.setWordWrap(True)
        content_layout.addWidget(self.title_display)

        # توضیحات
        self.description_display = QLabel()
        self.description_display.setWordWrap(True)
        self.description_display.setStyleSheet("margin-bottom: 12px;")
        content_layout.addWidget(self.description_display)

        # اطلاعات پروژه (نمایشی)
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
        info_display_layout.addRow("وضعیت:", self.status_display)

        self.progress_display = QLabel()
        info_display_layout.addRow("پیشرفت:", self.progress_display)

        self.tech_stack_display = QLabel()
        info_display_layout.addRow("تکنولوژی‌ها:", self.tech_stack_display)

        self.start_date_display = QLabel()
        info_display_layout.addRow("تاریخ شروع:", self.start_date_display)

        self.end_date_display = QLabel()
        info_display_layout.addRow("تاریخ پایان:", self.end_date_display)

        self.created_label = QLabel()
        info_display_layout.addRow("تاریخ ایجاد:", self.created_label)

        content_layout.addWidget(info_display_frame)

        # بخش ویرایش (پنهان به صورت پیش‌فرض)
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
        self.title_edit.setPlaceholderText("ویرایش عنوان پروژه")
        info_layout.addRow("عنوان:", self.title_edit)

        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText("توضیحات پروژه...")
        self.description_edit.setMinimumHeight(100)
        info_layout.addRow("توضیحات:", self.description_edit)

        self.status_combo = QComboBox()
        for label, value in self.status_options:
            self.status_combo.addItem(label, value)
        info_layout.addRow("وضعیت:", self.status_combo)

        self.progress_spin = QSpinBox()
        self.progress_spin.setRange(0, 100)
        self.progress_spin.setSuffix(" %")
        self.tech_stack_edit = QLineEdit()
        self.tech_stack_edit.setPlaceholderText("React, FastAPI, ...")
        info_layout.addRow("پیشرفت:", self.progress_spin)
        info_layout.addRow("تکنولوژی‌ها:", self.tech_stack_edit)

        self.start_date_edit = QLineEdit()
        self.start_date_edit.setPlaceholderText("YYYY-MM-DD")
        info_layout.addRow("تاریخ شروع:", self.start_date_edit)

        self.end_date_edit = QLineEdit()
        self.end_date_edit.setPlaceholderText("YYYY-MM-DD")
        info_layout.addRow("تاریخ پایان:", self.end_date_edit)

        edit_frame_layout.addLayout(info_layout)

        self.save_button = QPushButton("ذخیره تغییرات پروژه")
        self.save_button.clicked.connect(self.save_project_changes)
        edit_frame_layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.edit_form_frame.setVisible(False)
        content_layout.addWidget(self.edit_form_frame)

        self.toggle_edit_button = QPushButton("فعال‌سازی ویرایش")
        self.toggle_edit_button.clicked.connect(self.toggle_edit_mode)
        content_layout.addWidget(self.toggle_edit_button)

        self.step_summary_label = QLabel()
        self.step_summary_label.setStyleSheet("font-weight: bold; font-size: 15px; margin-top: 10px;")
        content_layout.addWidget(self.step_summary_label)

        board_title = QLabel("<b>تسک‌های پروژه</b>")
        board_title.setStyleSheet("font-size: 18px; margin-top: 6px;")
        content_layout.addWidget(board_title)

        self.board_layout = QHBoxLayout()
        self.board_layout.setSpacing(16)
        self.board_layout.setContentsMargins(0, 0, 0, 0)
        self.board_columns = {}
        for column_title, status_key in self.board_statuses:
            column = self._create_board_column(column_title, status_key)
            self.board_columns[status_key] = column
            self.board_layout.addWidget(column["frame"], 1)
        content_layout.addLayout(self.board_layout)

        content_layout.addStretch()

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def _create_board_column(self, title: str, status_key: str):
        column_frame = QFrame()
        column_frame.setStyleSheet("""
            QFrame {
                background-color: #0f1320;
                border-radius: 18px;
                border: 1px solid rgba(255, 255, 255, 0.04);
            }
        """)
        column_layout = QVBoxLayout(column_frame)
        column_layout.setContentsMargins(18, 18, 18, 18)
        column_layout.setSpacing(12)

        header = QLabel(title)
        header.setStyleSheet("font-size: 16px; font-weight: bold; color: #f5f6fb;")
        column_layout.addWidget(header)

        cards_container = QVBoxLayout()
        cards_container.setSpacing(12)
        column_layout.addLayout(cards_container)
        column_layout.addStretch()

        add_btn = QPushButton("+ افزودن کارت")
        add_btn.setEnabled(False)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.08);
                color: #d6d8e3;
                border-radius: 10px;
                padding: 10px 12px;
                font-weight: bold;
            }
        """)
        add_btn.clicked.connect(partial(self.open_add_step_dialog, status_key))
        column_layout.addWidget(add_btn)

        return {
            "frame": column_frame,
            "cards_layout": cards_container,
            "status": status_key,
            "header": header,
            "title": title,
            "add_button": add_btn,
        }

    def load_project_data(self):
        self.project = self.project_service.get(self.project_id)
        if not self.project:
            self.title_display.setText("پروژه یافت نشد")
            return

        # عنوان
        self.title_display.setText(f"<b>{self.project.title}</b>")
        self.title_edit.setText(self.project.title)

        # توضیحات
        description = self.project.description or self.project.summary or ""
        self.description_display.setText(f"<b>توضیحات:</b><br>{description or '---'}")
        self.description_edit.setPlainText(description)

        # وضعیت
        status_value = self.project.status or "todo"
        status_text = next((label for label, value in self.status_options if value == status_value), status_value)
        self.status_display.setText(status_text)
        idx = self.status_combo.findData(status_value)
        if idx >= 0:
            self.status_combo.setCurrentIndex(idx)

        # پیشرفت
        progress = self.project.progress or 0
        self.progress_display.setText(f"{progress}%")
        self.progress_spin.setValue(progress)

        # تکنولوژی‌ها
        tech_text = self.project.tech_stack or "تعریف نشده"
        self.tech_stack_display.setText(tech_text)
        self.tech_stack_edit.setText(self.project.tech_stack or "")

        # تاریخ‌ها
        start_text = self.format_date(self.project.start_date) or "تعریف نشده"
        end_text = self.format_date(self.project.end_date) or "تعریف نشده"
        self.start_date_display.setText(start_text)
        self.end_date_display.setText(end_text)
        self.start_date_edit.setText(self.format_date(self.project.start_date))
        self.end_date_edit.setText(self.format_date(self.project.end_date))

        # تاریخ ایجاد
        created_str = "-"
        if self.project.created_at:
            created_str = self.project.created_at.strftime("%Y-%m-%d %H:%M")
        self.created_label.setText(created_str)

        # بارگذاری مراحل پروژه
        self.load_steps()

    def load_steps(self):
        for column in self.board_columns.values():
            cards_layout = column["cards_layout"]
            while cards_layout.count():
                item = cards_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        self.steps_data = []

        steps = self.step_service.list_by_project(self.project_id)
        if not steps:
            self.step_summary_label.setText("هنوز تسکی برای این پروژه ثبت نشده است.")
            return

        self.steps_data = sorted(
            [
                {
                    "id": step_id,
                    "title": title,
                    "description": description,
                    "status": status,
                    "order": order or 0,
                }
                for step_id, title, description, status, order in steps
            ],
            key=lambda s: s["order"],
        )

        summary = {"todo": 0, "doing": 0, "done": 0}
        for step in self.steps_data:
            if step["status"] in summary:
                summary[step["status"]] += 1
        self.step_summary_label.setText(
            f"در انتظار: {summary['todo']} | در حال انجام: {summary['doing']} | انجام شده: {summary['done']}"
        )

        for _, status_key in self.board_statuses:
            column = self.board_columns[status_key]
            status_steps = [s for s in self.steps_data if s["status"] == status_key]
            column["header"].setText(f"{column['title']} ({len(status_steps)})")
            if not status_steps:
                empty_label = QLabel("کارت خالی")
                empty_label.setStyleSheet("color: #666; font-size: 12px;")
                column["cards_layout"].addWidget(empty_label)
                continue
            for idx, step in enumerate(status_steps):
                column["cards_layout"].addWidget(
                    self._build_step_card(step, idx, len(status_steps), self.edit_mode)
                )

    def _build_step_card(self, step: dict, position: int, total: int, editable: bool) -> QFrame:
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #1b2233;
                border-radius: 14px;
                padding: 14px;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }
        """)
        layout = QVBoxLayout(card)
        layout.setSpacing(8)

        title_label = QLabel(step["title"])
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #f7f7fb;")
        layout.addWidget(title_label)

        if step["description"]:
            desc_label = QLabel(step["description"])
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("color: #b8bfd3; font-size: 12px;")
            layout.addWidget(desc_label)

        order_label = QLabel(f"ترتیب: {step['order']}")
        order_label.setStyleSheet("color: #9499ab; font-size: 11px;")
        layout.addWidget(order_label)

        if editable:
            controls = QHBoxLayout()
            up_btn = QPushButton("▲")
            up_btn.setEnabled(position > 0)
            up_btn.clicked.connect(partial(self.move_step, step["id"], -1))
            up_btn.setStyleSheet("min-width: 32px; border-radius: 8px;")
            controls.addWidget(up_btn)

            down_btn = QPushButton("▼")
            down_btn.setEnabled(position < total - 1)
            down_btn.clicked.connect(partial(self.move_step, step["id"], 1))
            down_btn.setStyleSheet("min-width: 32px; border-radius: 8px;")
            controls.addWidget(down_btn)
            controls.addStretch()
            layout.addLayout(controls)

        return card

    def move_step(self, step_id: str, direction: int):
        if not self.edit_mode:
            return
        idx = next((i for i, step in enumerate(self.steps_data) if step["id"] == step_id), None)
        if idx is None:
            return

        status = self.steps_data[idx]["status"]
        same_status_indices = [i for i, step in enumerate(self.steps_data) if step["status"] == status]
        position = same_status_indices.index(idx)
        new_position = position + direction
        if new_position < 0 or new_position >= len(same_status_indices):
            return

        swap_idx = same_status_indices[new_position]
        self.steps_data[idx], self.steps_data[swap_idx] = self.steps_data[swap_idx], self.steps_data[idx]

        ordered_ids = [step["id"] for step in self.steps_data]
        self.step_service.reorder(self.project_id, ordered_ids)
        self.load_steps()

    def save_project_changes(self):
        title = self.title_edit.text().strip()
        if not title:
            QMessageBox.warning(self, "خطا", "عنوان پروژه نمی‌تواند خالی باشد.")
            return

        description = self.description_edit.toPlainText().strip()
        tech_stack = self.tech_stack_edit.text().strip()
        status = self.status_combo.currentData()
        progress = self.progress_spin.value()
        start_date = self.parse_date(self.start_date_edit.text().strip())
        end_date = self.parse_date(self.end_date_edit.text().strip())

        if self.start_date_edit.text().strip() and not start_date:
            QMessageBox.warning(self, "خطا", "فرمت تاریخ شروع باید YYYY-MM-DD باشد.")
            return
        if self.end_date_edit.text().strip() and not end_date:
            QMessageBox.warning(self, "خطا", "فرمت تاریخ پایان باید YYYY-MM-DD باشد.")
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
            QMessageBox.information(self, "ذخیره شد", "تغییرات با موفقیت ذخیره شد.")
            self.load_project_data()
        else:
            QMessageBox.warning(self, "خطا", "ذخیره تغییرات با مشکل مواجه شد.")

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
        self.toggle_edit_button.setText("لغو ویرایش" if enabled else "فعال‌سازی ویرایش")
        if hasattr(self, "board_columns"):
            for column in self.board_columns.values():
                column["add_button"].setEnabled(enabled)
        self.load_steps()

    def toggle_edit_mode(self):
        self.set_edit_mode(not self.edit_mode)

    def _next_order_for(self, status_key: str) -> int:
        status_orders = [step["order"] for step in self.steps_data if step["status"] == status_key]
        return max(status_orders, default=0) + 1

    def open_add_step_dialog(self, status_key: str):
        if not self.edit_mode:
            QMessageBox.information(self, "ویرایش غیرفعال", "برای افزودن مرحله جدید، حالت ویرایش را فعال کنید.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("افزودن مرحله جدید")
        layout = QVBoxLayout(dialog)
        layout.setSpacing(12)

        layout.addWidget(QLabel("عنوان"))
        title_edit = QLineEdit()
        title_edit.setPlaceholderText("عنوان مرحله")
        layout.addWidget(title_edit)

        layout.addWidget(QLabel("توضیحات"))
        desc_edit = QTextEdit()
        desc_edit.setPlaceholderText("توضیحات مرحله...")
        desc_edit.setMinimumHeight(80)
        layout.addWidget(desc_edit)

        layout.addWidget(QLabel("ترتیب"))
        order_spin = QSpinBox()
        order_spin.setRange(1, 999)
        order_spin.setValue(self._next_order_for(status_key))
        layout.addWidget(order_spin)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        layout.addWidget(button_box)

        def handle_accept():
            title = title_edit.text().strip()
            if not title:
                QMessageBox.warning(dialog, "خطا", "عنوان مرحله نمی‌تواند خالی باشد.")
                return
            description = desc_edit.toPlainText().strip()
            order_value = order_spin.value()
            self.step_service.add(
                project_id=self.project_id,
                title=title,
                description=description,
                status=status_key,
                order=order_value,
            )
            dialog.accept()

        button_box.accepted.connect(handle_accept)
        button_box.rejected.connect(dialog.reject)

        if dialog.exec():
            self.load_steps()

