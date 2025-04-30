# Taskora (formerly TodoList PyQt6)

&#x20;

A personal assistant application for task management, journaling, and time tracking, built with PyQt6, SQLAlchemy, and Alembic following the MVVM pattern.

---

## 📋 Table of Contents

- [🚀 Features](#-features)
- [🧩 Architecture](#-architecture)
- [⚙️ Prerequisites](#️-prerequisites)
- [💾 Installation & Setup](#-installation--setup)
- [▶️ Running the Application](#️-running-the-application)
- [🔄 Database Migrations](#-database-migrations)
- [🧪 Usage Examples](#-usage-examples)
- [🖼️ Screenshots](#️-screenshots)
- [🔧 Configuration](#-configuration)
- [🛠️ Development Dependencies](#️-development-dependencies)
- [📂 Project Structure](#-project-structure)
- [🛣️ Roadmap](#️-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [✉️ Contact](#️-contact)

---

## 🚀 Features

- **Guest mode (current)**: store tasks and data locally in JSON files
- Dark and light theme support via QSS
- Desktop notifications and system tray integration

---

## 🧩 Architecture

This project follows the **MVVM** pattern to maintain clear separation of

- **View**: UI definitions in `views/` (pages and widgets)
- **ViewModel**: Binding and presentation logic in `viewmodels/`
- **Model**: Data models in `models/` and ORM mappings in `mapper/`
- **Controllers**: Request coordination in `controllers/`
- **Services**: Business logic and data access in `services/`
- **Core & Utils**: Session management and helper functions in `core/` and `utils/`

---

## ⚙️ Prerequisites

- **Python** 3.8 or higher
- **pip**
- **Git**

---

## 💾 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/alibahrami1376/Todolist_byPyQt.git
   cd Todolist_byPyQt
   ```
2. **Create & activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1
   ```
3. **Install runtime dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **(Optional) Install dev dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

---

## ▶️ Running the Application

1. **Apply DB migrations**
   ```bash
   alembic upgrade head
   ```
2. **Launch**
   ```bash
   python main.py
   ```

---

## 🔄 Database Migrations

Migration scripts: `alembic/versions/`

- Generate new migration:
  ```bash
  alembic revision --autogenerate -m "Describe changes"
  alembic upgrade head
  ```

---

## 🧪 Usage Examples

```bash
# Add a new task via UI Start
python main.py
```

1. Open **New Task** dialog
2. Enter **Title**, **Description**, **Due Date**, **Tags**, **Priority**
3. Click **Save**

```bash
# Time tracking example
# In the task details view, click ▶ Start Timer, ▶ Stop Timer, and view total time logged.
```

---

## 🖼️ Screenshots



---

## 🔧 Configuration

Configuration file: `config/settings.json`

```json
{
  "database_url": "sqlite:///data/tasks.db",
  "notify_tray": true,
  "theme": "dark"
}
```

---

## 🛠️ Development Dependencies

Listed in `requirements-dev.txt`:

- **pytest** for tests
- **pyinstaller**, **altgraph**, **pefile** for packaging
- **flake8**, **black** for linting

---

## 📂 Project Structure

```
Todolist_byPyQt/
├── alembic/             # DB migration scripts & config
├── config/              # Application settings
├── controllers/         # Request handlers
├── core/                # Session & base logic
├── data/                # Local DB and seed files
├── docs/                # Documentation & assets
├── mapper/              # ORM mapping
├── models/              # Data models
├── services/            # Business logic
├── styles/              # QSS theme files
├── utils/               # Helpers
├── viewmodels/          # Presentation logic
├── views/               # UI definitions
├── tests/               # Unit and integration tests
├── main.py              # Entry point
├── requirements.txt
├── requirements-dev.txt
├── alembic.ini
├── ci.yml               # GitHub Actions workflow
├── README.md
└── .gitignore
```

---

## 🛣️ Roadmap

- **User mode with registration and login** (coming soon)
- **Time tracking and journaling per task** (coming soon)
- Recurring tasks scheduler
- Time-journal export (CSV/PDF)
- Cloud sync via REST API
- Mobile companion app

