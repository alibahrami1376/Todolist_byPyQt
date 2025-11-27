from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QScrollArea,
    QWidget,
    QFrame,
    QCheckBox,
    QLineEdit,
    QTextEdit,
    QSpinBox,
    QMessageBox,
    QDialogButtonBox,
    QComboBox,
)
from PyQt6.QtCore import Qt

from services.project_service import ProjectService
from services.project_step_service import ProjectStepService


class ProjectStepsDialog(QDialog):
    def __init__(self, project_id: str):
        super().__init__()
        self.project_id = project_id
        self.project_service = ProjectService()
        self.step_service = ProjectStepService()
        self.steps_data = []
        self.board_statuses = [
            ("Backlog", "todo"),
            ("In Progress", "doing"),
            ("Done", "done"),
        ]
        self.status_lookup = {
            "todo": "Backlog",
            "doing": "In Progress",
            "done": "Done",
        }
        self.edit_mode = False

        self.setWindowTitle("Project Steps")
        self.setMinimumSize(720, 520)
        self.setWindowFlag(Qt.WindowType.WindowMinMaxButtonsHint, True)
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, True)

        self._init_ui()
        self.load_project_meta()
        self.set_edit_mode(False)

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(14)

        header = QHBoxLayout()
        self.project_title_lbl = QLabel()
        self.project_title_lbl.setStyleSheet("font-size: 22px; font-weight: 600;")
        header.addWidget(self.project_title_lbl)
        header.addStretch()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        header.addWidget(close_btn)
        main_layout.addLayout(header)

        self.project_meta_lbl = QLabel()
        self.project_meta_lbl.setStyleSheet("color: #9aa0b5;")
        main_layout.addWidget(self.project_meta_lbl)

        self.toggle_edit_button = QPushButton("Enable editing")
        self.toggle_edit_button.clicked.connect(self.toggle_edit_mode)
        main_layout.addWidget(self.toggle_edit_button)

        self.step_summary_label = QLabel()
        self.step_summary_label.setStyleSheet("font-weight: 600; font-size: 15px;")
        main_layout.addWidget(self.step_summary_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        main_layout.addWidget(scroll, 1)

        content = QWidget()
        scroll_layout = QHBoxLayout(content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(16)

        self.board_columns = {}
        for title, status in self.board_statuses:
            column = self._create_board_column(title, status)
            self.board_columns[status] = column
            scroll_layout.addWidget(column["frame"], 1)

        scroll_layout.addStretch()
        scroll.setWidget(content)

    def load_project_meta(self):
        project = self.project_service.get(self.project_id)
        if not project:
            self.project_title_lbl.setText("Project not found")
            self.project_meta_lbl.setText("")
            return
        self.project_title_lbl.setText(project.title)
        created = "-"
        if project.created_at:
            created = project.created_at.strftime("%Y-%m-%d %H:%M")
        self.project_meta_lbl.setText(f"Created at {created} • Status: {project.status or 'todo'}")
        self.load_steps()

    def _create_board_column(self, title: str, status_key: str):
        column_frame = QFrame()
        column_frame.setStyleSheet(
            """
            QFrame {
                background-color: #0f1320;
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.06);
            }
        """
        )
        column_layout = QVBoxLayout(column_frame)
        column_layout.setContentsMargins(12, 12, 12, 12)
        column_layout.setSpacing(8)

        header = QLabel(title)
        header.setStyleSheet("font-size: 15px; font-weight: bold; color: #f5f6fb; padding-bottom: 4px;")
        column_layout.addWidget(header)

        cards_widget = QWidget()
        cards_layout = QVBoxLayout(cards_widget)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(8)
        cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        column_layout.addWidget(cards_widget, 1)

        add_btn = QPushButton("+ Add card")
        add_btn.setEnabled(False)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setFixedHeight(36)
        add_btn.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.08);
                color: #d6d8e3;
                border-radius: 8px;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:enabled:hover {
                background-color: rgba(255, 255, 255, 0.12);
            }
            QPushButton:disabled {
                background-color: rgba(255, 255, 255, 0.04);
                color: #737a94;
            }
        """
        )
        add_btn.clicked.connect(lambda _, status=status_key: self.open_add_step_dialog(status))
        column_layout.addWidget(add_btn, 0)

        return {
            "frame": column_frame,
            "cards_layout": cards_layout,
            "status": status_key,
            "header": header,
            "title": title,
            "add_button": add_btn,
        }

    def load_steps(self):
        for column in self.board_columns.values():
            layout = column["cards_layout"]
            # Remove stretch first
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
                elif item.spacerItem():
                    layout.removeItem(item)

        steps = self.step_service.list_by_project(self.project_id)
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

        if not self.steps_data:
            self.step_summary_label.setText("No steps recorded yet.")
        else:
            summary = {"todo": 0, "doing": 0, "done": 0}
            for step in self.steps_data:
                if step["status"] in summary:
                    summary[step["status"]] += 1
            self.step_summary_label.setText(
                f"Backlog: {summary['todo']} | In Progress: {summary['doing']} | Done: {summary['done']}"
            )

        for _, status_key in self.board_statuses:
            column = self.board_columns[status_key]
            steps_for_column = [s for s in self.steps_data if s["status"] == status_key]
            column["header"].setText(f"{column['title']} ({len(steps_for_column)})")
            if not steps_for_column:
                placeholder = QLabel("Empty")
                placeholder.setStyleSheet("color: #737a94; font-size: 11px; padding: 8px;")
                placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
                column["cards_layout"].addWidget(placeholder, 0, Qt.AlignmentFlag.AlignTop)
            else:
                for index, step in enumerate(steps_for_column):
                    column["cards_layout"].addWidget(
                        self._build_step_card(step, index, len(steps_for_column)),
                        0,
                        Qt.AlignmentFlag.AlignTop
                    )

    def _build_step_card(self, step: dict, position: int, total: int) -> QFrame:
        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color: #151b2a;
                border-radius: 10px;
                padding: 0px;
                border: 1px solid rgba(255, 255, 255, 0.05);
            }
        """
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header with title and expand button
        header = QFrame()
        header.setStyleSheet("background-color: transparent; padding: 10px;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 10, 10, 10)
        header_layout.setSpacing(8)

        title_label = QLabel(step["title"])
        title_label.setStyleSheet("font-weight: 600; font-size: 13px; color: #f7f7fb;")
        header_layout.addWidget(title_label, 1)

        expand_btn = QPushButton("▼")
        expand_btn.setCheckable(True)
        expand_btn.setChecked(False)
        expand_btn.setFixedSize(24, 24)
        expand_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        expand_btn.setStyleSheet(
            """
            QPushButton {
                border-radius: 4px;
                background-color: rgba(255, 255, 255, 0.08);
                color: #cfd3e2;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.15);
            }
            QPushButton:checked {
                background-color: rgba(59, 130, 246, 0.2);
                color: #60a5fa;
            }
        """
        )
        header_layout.addWidget(expand_btn, 0)
        layout.addWidget(header)

        # Expandable content container
        content_widget = QWidget()
        content_widget.setVisible(False)
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(10, 0, 10, 10)
        content_layout.setSpacing(6)

        if step["description"]:
            desc_label = QLabel(step["description"])
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("color: #b8bfd3; font-size: 11px;")
            content_layout.addWidget(desc_label)

        order_label = QLabel(f"Order: {step['order']}")
        order_label.setStyleSheet("color: #8c92a5; font-size: 10px;")
        content_layout.addWidget(order_label)

        next_status = self._next_step_status(step["status"])
        prev_status = self._previous_step_status(step["status"])
        if next_status:
            next_label = self.status_lookup.get(next_status, next_status)
            content_layout.addLayout(
                self._build_status_checkbox(
                    f'Move to "{next_label}"',
                    lambda state, sid=step["id"], cur=step["status"]: self._handle_progress(sid, cur, state),
                )
            )
        if prev_status:
            prev_label = self.status_lookup.get(prev_status, prev_status)
            content_layout.addLayout(
                self._build_status_checkbox(
                    f'Return to "{prev_label}"',
                    lambda state, sid=step["id"], cur=step["status"]: self._handle_regress(sid, cur, state),
                )
            )

        if self.edit_mode:
            controls = QHBoxLayout()
            controls.setSpacing(6)
            edit_btn = QPushButton("Edit")
            edit_btn.setEnabled(True)
            edit_btn.clicked.connect(lambda _, sid=step["id"]: self.open_edit_step_dialog(sid))
            edit_btn.setStyleSheet(
                """
                QPushButton {
                    padding: 4px 12px;
                    border-radius: 6px;
                    background-color: rgba(59, 130, 246, 0.15);
                    color: #60a5fa;
                    font-size: 11px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: rgba(59, 130, 246, 0.25);
                }
            """
            )
            controls.addWidget(edit_btn)
            controls.addStretch()
            delete_btn = QPushButton("Delete")
            delete_btn.setEnabled(True)
            delete_btn.clicked.connect(lambda _, sid=step["id"]: self.delete_step(sid))
            delete_btn.setStyleSheet(
                """
                QPushButton {
                    padding: 4px 12px;
                    border-radius: 6px;
                    background-color: rgba(244, 63, 94, 0.15);
                    color: #f43f5e;
                    font-size: 11px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: rgba(244, 63, 94, 0.25);
                }
            """
            )
            controls.addWidget(delete_btn)
            content_layout.addLayout(controls)

        layout.addWidget(content_widget)

        # Connect expand button
        def toggle_expand(checked):
            content_widget.setVisible(checked)
            expand_btn.setText("▲" if checked else "▼")

        expand_btn.toggled.connect(toggle_expand)

        return card

    def _build_status_checkbox(self, text: str, handler):
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)
        row.setSpacing(6)
        checkbox = QCheckBox(text)
        checkbox.setCursor(Qt.CursorShape.PointingHandCursor)
        checkbox.setStyleSheet("color: #cfd3e2; font-size: 11px;")
        checkbox.stateChanged.connect(handler)
        row.addWidget(checkbox)
        row.addStretch()
        return row

    def _handle_progress(self, step_id: str, current_status: str, state: int):
        if state != Qt.CheckState.Checked.value:
            return
        self.advance_step(step_id, current_status)

    def _handle_regress(self, step_id: str, current_status: str, state: int):
        if state != Qt.CheckState.Checked.value:
            return
        self.regress_step(step_id, current_status)

    def _next_step_status(self, status: str) -> str | None:
        pipeline = ["todo", "doing", "done"]
        try:
            index = pipeline.index(status)
        except ValueError:
            return None
        if index == len(pipeline) - 1:
            return None
        return pipeline[index + 1]

    def _previous_step_status(self, status: str) -> str | None:
        pipeline = ["todo", "doing", "done"]
        try:
            index = pipeline.index(status)
        except ValueError:
            return None
        if index == 0:
            return None
        return pipeline[index - 1]

    def advance_step(self, step_id: str, current_status: str):
        next_status = self._next_step_status(current_status)
        if not next_status:
            return
        self.step_service.update_status(step_id, next_status)
        self.load_steps()

    def regress_step(self, step_id: str, current_status: str):
        prev_status = self._previous_step_status(current_status)
        if not prev_status:
            return
        self.step_service.update_status(step_id, prev_status)
        self.load_steps()

    def move_step(self, step_id: str, direction: int):
        if not self.edit_mode:
            return
        current_idx = next((i for i, step in enumerate(self.steps_data) if step["id"] == step_id), None)
        if current_idx is None:
            return
        status = self.steps_data[current_idx]["status"]
        same_status_indices = [i for i, step in enumerate(self.steps_data) if step["status"] == status]
        position = same_status_indices.index(current_idx)
        new_position = position + direction
        if new_position < 0 or new_position >= len(same_status_indices):
            return

        swap_idx = same_status_indices[new_position]
        self.steps_data[current_idx], self.steps_data[swap_idx] = self.steps_data[swap_idx], self.steps_data[current_idx]
        
        # After swap, rebuild order values for ALL steps based on their positions in self.steps_data
        # Group steps by status, preserving their order within self.steps_data
        status_groups = {}
        for idx, step in enumerate(self.steps_data):
            if step["status"] not in status_groups:
                status_groups[step["status"]] = []
            status_groups[step["status"]].append((idx, step))
        
        # Build ordered list: group by status, maintain order within each status from self.steps_data
        all_ordered = []
        for status_key in ["todo", "doing", "done"]:
            if status_key in status_groups:
                # Sort by original index in self.steps_data to preserve the order after swap
                sorted_by_index = sorted(status_groups[status_key], key=lambda x: x[0])
                all_ordered.extend([step for _, step in sorted_by_index])
        
        # Assign sequential order values
        for idx, step in enumerate(all_ordered, start=1):
            step["order"] = idx
        
        # Update in database
        ordered_ids = [step["id"] for step in all_ordered]
        self.step_service.reorder(self.project_id, ordered_ids)
        self.load_steps()

    def set_edit_mode(self, enabled: bool):
        self.edit_mode = enabled
        self.toggle_edit_button.setText("Cancel editing" if enabled else "Enable editing")
        for column in self.board_columns.values():
            column["add_button"].setEnabled(enabled)
        self.load_steps()

    def toggle_edit_mode(self):
        self.set_edit_mode(not self.edit_mode)

    def _next_order_for(self, status_key: str) -> int:
        orders = [step["order"] for step in self.steps_data if step["status"] == status_key]
        return max(orders, default=0) + 1

    def open_add_step_dialog(self, status_key: str):
        if not self.edit_mode:
            QMessageBox.information(self, "Editing disabled", "Enable editing before adding a new step.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Add new step")
        layout = QVBoxLayout(dialog)
        layout.setSpacing(12)

        layout.addWidget(QLabel("Title"))
        title_edit = QLineEdit()
        title_edit.setPlaceholderText("Step title")
        layout.addWidget(title_edit)

        layout.addWidget(QLabel("Description"))
        desc_edit = QTextEdit()
        desc_edit.setPlaceholderText("Describe the outcome of this step")
        desc_edit.setMinimumHeight(80)
        layout.addWidget(desc_edit)

        layout.addWidget(QLabel("Order"))
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
                QMessageBox.warning(dialog, "Missing title", "Step title cannot be empty.")
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

    def open_edit_step_dialog(self, step_id: str):
        if not self.edit_mode:
            QMessageBox.information(self, "Editing disabled", "Enable editing before editing a step.")
            return

        step = self.step_service.get(step_id)
        if not step:
            QMessageBox.warning(self, "Not found", "Step not found.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Edit step")
        layout = QVBoxLayout(dialog)
        layout.setSpacing(12)

        layout.addWidget(QLabel("Title"))
        title_edit = QLineEdit()
        title_edit.setText(step.title or "")
        title_edit.setPlaceholderText("Step title")
        layout.addWidget(title_edit)

        layout.addWidget(QLabel("Description"))
        desc_edit = QTextEdit()
        desc_edit.setPlainText(step.description or "")
        desc_edit.setPlaceholderText("Describe the outcome of this step")
        desc_edit.setMinimumHeight(80)
        layout.addWidget(desc_edit)

        layout.addWidget(QLabel("Status"))
        status_combo = QComboBox()
        for title, status in self.board_statuses:
            status_combo.addItem(title, status)
        current_idx = status_combo.findData(step.status or "todo")
        if current_idx >= 0:
            status_combo.setCurrentIndex(current_idx)
        layout.addWidget(status_combo)

        layout.addWidget(QLabel("Order"))
        order_spin = QSpinBox()
        order_spin.setRange(1, 999)
        order_spin.setValue(step.order or 1)
        layout.addWidget(order_spin)

        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        layout.addWidget(button_box)

        def handle_accept():
            title = title_edit.text().strip()
            if not title:
                QMessageBox.warning(dialog, "Missing title", "Step title cannot be empty.")
                return
            description = desc_edit.toPlainText().strip()
            status_value = status_combo.currentData()
            order_value = order_spin.value()
            
            updated = self.step_service.update(
                step_id=step_id,
                title=title,
                description=description,
                status=status_value,
                order=order_value
            )
            if not updated:
                QMessageBox.warning(dialog, "Error", "Failed to update step.")
                return
            dialog.accept()

        button_box.accepted.connect(handle_accept)
        button_box.rejected.connect(dialog.reject)

        if dialog.exec():
            self.load_steps()

    def delete_step(self, step_id: str):
        if not self.edit_mode:
            return
        
        confirm = QMessageBox.question(
            self,
            "Delete Step",
            "Are you sure you want to delete this step?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return
        
        self.step_service.delete(step_id)
        self.load_steps()

