# Slack Message Cleaner UI

A graphical user interface (GUI) implementation of the Slack Cleaner tool using PyQT5

---

## Installation

```bash
pip install slack-cleaner2 PyQt5 pyinstaller
```

---

## Release Notes
1. Added filtering to only display and delete user's own messages.
2. Implemented remove and skip functionality for selective message deletion.

---

## Deployment

```bash
pyinstaller --onefile main.py
```