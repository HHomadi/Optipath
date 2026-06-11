import os
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent

# Database
DATABASE_PATH = os.environ.get("OPTIPATH_DB", str(CODE_DIR / "user_accounts.db"))

# Email (verification) – set OPTIPATH_EMAIL and OPTIPATH_EMAIL_PASSWORD in env
SMTP_SERVER = os.environ.get("OPTIPATH_SMTP_SERVER", "smtp.office365.com")
SMTP_PORT = int(os.environ.get("OPTIPATH_SMTP_PORT", "587"))
SENDER_EMAIL = os.environ.get("OPTIPATH_EMAIL", "")
SENDER_PASSWORD = os.environ.get("OPTIPATH_EMAIL_PASSWORD", "")

IMAGES_DIR = CODE_DIR / "static" / "images"
GRAPHS_DIR = CODE_DIR / "Graphs"
FLASK_URL = os.environ.get("OPTIPATH_FLASK_URL", "http://127.0.0.1:5000")
