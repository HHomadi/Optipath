"""
Centralised database access for user accounts, auth and sessions.
All DB usage should go through this module.
"""
import sqlite3
import random
import smtplib
import hashlib
from typing import Optional
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import (
    DATABASE_PATH,
    FLASK_URL,
    SMTP_SERVER,
    SMTP_PORT,
    SENDER_EMAIL,
    SENDER_PASSWORD,
)

def _error(text: str) -> None:
    print("\033[91m {}\033[00m".format(text))

class Database:
    """Single place for all database access."""

    def __init__(self, db_path: Optional[str] = None):
        self._path = db_path or DATABASE_PATH
        self._conn = sqlite3.connect(self._path)
        self._cursor = self._conn.cursor()
        self._create_tables()

    def _create_tables(self) -> None:
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT(15) NOT NULL UNIQUE,
                email TEXT(255) NOT NULL UNIQUE
            )
        """)
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_authentication (
                user_id INTEGER PRIMARY KEY,
                password TEXT NOT NULL,
                verification_code TEXT,
                is_verified INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                user_id INTEGER PRIMARY KEY,
                currently_logged_in INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        self._conn.commit()

    def create_account(self, username: str, email: str, password: str) -> bool:
        try:
            verification_code = str(random.randint(111111, 999999))
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            self._cursor.execute(
                "INSERT INTO users (username, email) VALUES (?, ?)",
                (username, email),
            )
            user_id = self._cursor.lastrowid
            self._cursor.execute(
                "INSERT INTO user_authentication (user_id, password, verification_code) VALUES (?, ?, ?)",
                (user_id, password_hash, verification_code),
            )
            self._cursor.execute("INSERT INTO user_sessions (user_id) VALUES (?)", (user_id,))
            self._conn.commit()

            verification_link = f"{FLASK_URL}/verify/{user_id}/{verification_code}"
            self._send_verification_email(email, verification_link, username)
            return True
        except sqlite3.IntegrityError:
            return False

    def get_user_data_by_username(self, username: str) -> Optional[dict]:
        self._cursor.execute("""
            SELECT u.username, u.email, ua.password, ua.verification_code, ua.is_verified, us.currently_logged_in
            FROM users u
            JOIN user_authentication ua ON u.user_id = ua.user_id
            LEFT JOIN user_sessions us ON u.user_id = us.user_id
            WHERE u.username = ?
        """, (username,))
        row = self._cursor.fetchone()
        if not row:
            return None
        return {
            "username": row[0],
            "email": row[1],
            "password": row[2],
            "verification_code": row[3],
            "is_verified": row[4],
            "currently_logged_in": row[5],
        }

    def get_user_id_by_username(self, username: str) -> Optional[int]:
        self._cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        row = self._cursor.fetchone()
        return row[0] if row else None

    def valid_username(self, username: str) -> bool:
        self._cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
        return self._cursor.fetchone()[0] == 0

    def update_password_by_email(self, email: str, new_password_hash: str) -> bool:
        try:
            self._cursor.execute(
                "UPDATE user_authentication SET password = ? WHERE user_id IN (SELECT user_id FROM users WHERE email = ?)",
                (new_password_hash, email),
            )
            if self._cursor.rowcount > 0:
                self._conn.commit()
                return True
            return False
        except Exception:
            return False

    def set_logged_in_user(self, user_id: Optional[int]) -> None:
        self._cursor.execute("UPDATE user_sessions SET currently_logged_in = 0")
        if user_id is not None:
            self._cursor.execute(
                "UPDATE user_sessions SET currently_logged_in = 1 WHERE user_id = ?",
                (user_id,),
            )
        self._conn.commit()

    def get_logged_in_user_id(self) -> Optional[int]:
        self._cursor.execute("SELECT user_id FROM user_sessions WHERE currently_logged_in = 1")
        row = self._cursor.fetchone()
        return row[0] if row else None

    def verify_account(self, user_id: int, verification_code: str) -> bool:
        self._cursor.execute("""
            UPDATE user_authentication
            SET is_verified = 1
            WHERE user_id = ? AND verification_code = ?
        """, (user_id, verification_code))
        updated = self._cursor.rowcount > 0
        if updated:
            self._conn.commit()
        return updated

    def _send_verification_email(self, recipient_email: str, verification_link: str, username: str) -> None:
        if not SENDER_EMAIL or not SENDER_PASSWORD:
            _error("OPTIPATH_EMAIL and OPTIPATH_EMAIL_PASSWORD must be set to send verification emails.")
            return
        subject = "Email Verification"
        html_content = f"""
        <html>
        <body>
            <p>Thank you for registering an OptiPath account</p>
            <p>Your account information:</p>
            <p>Username: {username}</p>
            <p>Please click the link below to activate your account:</p>
            <p><a href="{verification_link}">{verification_link}</a></p>
            <p>If you did not request this, you can safely ignore this email.</p>
            <p>Regards,<br>OptiPath</p>
            <img src="https://i.imgur.com/JIp00oS.png" alt="OptiPath Logo">
        </body>
        </html>
        """
        server = None
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            msg = MIMEMultipart("alternative")
            msg["From"] = SENDER_EMAIL
            msg["To"] = recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(html_content, "html"))
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        except smtplib.SMTPAuthenticationError:
            _error("SMTP Authentication Error: check OPTIPATH_EMAIL and OPTIPATH_EMAIL_PASSWORD.")
        except smtplib.SMTPException as e:
            _error("SMTP Exception: {}".format(e))
        except Exception as e:
            _error("Error sending verification email: {}".format(e))
        finally:
            if server:
                try:
                    server.quit()
                except Exception:
                    pass

    def close(self) -> None:
        self._conn.close()

DatabaseSetup = Database  # backwards compatibility
