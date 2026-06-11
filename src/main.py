import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from GUI import GUI
from database import Database
import hashlib
import subprocess

"""
Main entry point for the OptiPath desktop app.
Runs the PyQt GUI and starts the Flask server for the embedded website.
"""

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = GUI()
        self.ui.setupUi(self)

        self.db = Database()
        self.flask_process = None
        self.start_flask_server()

        self.ui.loginButton.clicked.connect(self.login)
        self.ui.createAnAccount.clicked.connect(self.create_account)
        self.ui.resetPasswordForgotPassword.clicked.connect(self.reset_password)

    def start_flask_server(self) -> None:
        code_dir = os.path.dirname(os.path.abspath(__file__))
        self.flask_process = subprocess.Popen([sys.executable, "app.py"], cwd=code_dir)
    def login(self) -> None:
        username = self.ui.username.text()
        password = self.ui.password.text()

        user_data = self.db.get_user_data_by_username(username)

        if user_data:
            if user_data["is_verified"] == 0:
                self.show_message("Account Not Verified", "Please verify your email first.", QMessageBox.Warning)
            else:
                provided_password_hash = hashlib.sha256(password.encode()).hexdigest()

                if provided_password_hash == user_data["password"]:
                    try:
                        user_id = self.db.get_user_id_by_username(username)
                        if user_id is not None:
                            self.db.set_logged_in_user(user_id)
                        self.show_message("Login Successful", "You have successfully logged in.", QMessageBox.Information)
                        self.ui.stackedWidget.setCurrentIndex(3)
                    except Exception as e:
                        print("Error updating login status: {}".format(e))
                else:
                    self.show_message("Login Failed", "Invalid username or password.", QMessageBox.Warning)
        else:
            self.show_message("Login Failed", "Invalid username or password.", QMessageBox.Warning)

    def create_account(self) -> None:
        username = self.ui.usernameCreate.text()
        email = self.ui.emailCreate.text()
        password = self.ui.passwordCreate.text()

        if not self.db.valid_username(username):
            self.show_message("Invalid Username", "Please enter a valid username.", QMessageBox.Warning)
            return
        if not self.is_valid_email(email):
            self.show_message("Invalid Email", "Please enter a valid email address.", QMessageBox.Warning)
            return

        if not self.is_valid_password(password):
            self.show_message("Invalid Password", "Password must have at least 8 characters, "
                             "a capital letter, a special character, and both uppercase and lowercase letters.", QMessageBox.Warning)
            return

        # create the account
        if self.db.create_account(username, email, password):
            self.show_message("Account Created", "Your account has been successfully created.", QMessageBox.Information)
        else:
            self.show_message("Account Creation Failed", "Username or email already exists.", QMessageBox.Warning)
        self.ui.clear_line()

    def reset_password(self) -> None:
        email = self.ui.emailForgot.text()
        new_password = self.ui.newPassword.text()
        password_hash = hashlib.sha256(new_password.encode()).hexdigest()

        # Check email and password validity
        if not self.is_valid_email(email):
            self.show_message("Invalid Email", "Please enter a valid email address.", QMessageBox.Warning)
            return

        if not self.is_valid_password(new_password):
            self.show_message("Invalid Password", "Password must have at least 8 characters, "
                             "a capital letter, a special character, and both uppercase and lowercase letters.", QMessageBox.Warning)
            return

        if self.db.update_password_by_email(email, password_hash):
            self.show_message("Password Reset", "Your password has been reset successfully.", QMessageBox.Information)
        else:
            self.show_message("Password Reset Failed", "Email not found or password update failed.", QMessageBox.Warning)

    def is_valid_email(self, email: str) -> bool:
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return True if re.match(email_pattern, email) else False

    def is_valid_password(self, password: str) -> bool:
        if len(password) < 8:
            return False
        if not any(x.isupper() for x in password):
            return False
        if not any(x.islower() for x in password):
            return False
        if not any(x.isdigit() for x in password):
            return False
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for c in password):
            return False
        return True

    def show_message(self, title: str, message: str, icon) -> None:
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        msg_box.exec_()

def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    window.setWindowTitle("OptiPath")
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()