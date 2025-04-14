# Todolist_byPyQt
I'm writing a todo list application with pyqt6.
# 🧭 Widget Structure Documentation (PyQt Todo App - MVVM)

## 📌 Main Window: `PageManagerWindow` (`QMainWindow`)

Acts as the main frame of the application. Inherits from `QMainWindow` and manages the view switching using an internal `QStackedWidget`.

---

## 📄 Pages Inside `PageManagerWindow`

### ✅ `LoginPage` (`QWidget`)
**Purpose:** Basic login interface

- `QLabel` – Title: "Login"
- `QLineEdit` – Username input
- `QLineEdit` – Password input
- `QPushButton` – Login and Exit

⚠️ Uses `QMessageBox` to warn about incorrect username/password.

---

### ✅ `TaskManagerWindow` (`QMainWindow` or `QWidget`)
**Purpose:** Main task management interface

- `QLineEdit` – Quick task input
- `QPushButton` – Add and "More" buttons
- `QListWidget` – Task list display
- `QPushButton` – Delete and Clear All

⚠️ Shows `QMessageBox` when trying to delete without selection.

---

## ➕ `AddTaskWindow` (`QDialog`)
**Purpose:** Add/edit task with full details

- `QLineEdit` – Task title
- `QTextEdit` – Description
- `QComboBox` – Priority selector
- `QDateEdit` – Due date picker
- `QCheckBox` – Subtask checkbox
- `QPushButton` – Save task

⚠️ Shows `QMessageBox` if title is left empty.

---

## ⚠️ Shared Warning System: `QMessageBox`

Used across all pages for error/warning dialogs:
- Failed login
- Deleting without selection
- Saving a task without title

---

## 🧠 Summary

This UI structure is:

- ✅ Modular and maintainable
- ✅ Based on `QMainWindow` with `QStackedWidget` for multi-page control
- ✅ Uses standard widgets with `QMessageBox` for consistent UX

