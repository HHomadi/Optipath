from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QCursor
from graphPlot import GraphVisualiser
from config import IMAGES_DIR

class GUI:
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.stackedWidget.setObjectName("stackedWidget")

        # login page

        self.login = QtWidgets.QWidget()
        self.login.setObjectName("login")

        self.background = QtWidgets.QLabel(self.login)
        self.background.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.background.setText("")
        self.background.setPixmap(QtGui.QPixmap(str(IMAGES_DIR / "Login.background.labelled.png")))


        self.username = QtWidgets.QLineEdit(self.login)
        self.username.setGeometry(QtCore.QRect(699, 330, 523, 70))
        self.username.setFont(QtGui.QFont("Montserrat Medium", 10))
        self.username.setStyleSheet("QLineEdit { background: rgba(0, 0, 0, 0); color: #CCCCCC; border: 1px solid transparent; }")

        self.password = QtWidgets.QLineEdit(self.login)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setGeometry(QtCore.QRect(699, 410, 523, 70))
        self.password.setFont(QtGui.QFont("Montserrat Medium", 10))
        self.password.setStyleSheet("QLineEdit { background: rgba(0, 0, 0, 0); color: #CCCCCC; border: 1px solid transparent; }")

        self.createAnAccountLogin = QtWidgets.QPushButton(self.login)
        self.createAnAccountLogin.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.createAnAccountLogin.setGeometry(QtCore.QRect(700, 489, 202, 41))
        self.createAnAccountLogin.setText("Create An Account")

        self.forgotPassword = QtWidgets.QPushButton(self.login)
        self.forgotPassword.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.forgotPassword.setGeometry(QtCore.QRect(1019, 489, 202, 40))
        self.forgotPassword.setText("Forgot Password")

        self.loginButton = QtWidgets.QPushButton(self.login)
        self.loginButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.loginButton.setGeometry(QtCore.QRect(699, 550, 523, 39))
        self.loginButton.setText("Login")

        self.exitButton = QtWidgets.QPushButton(self.login)
        self.exitButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.exitButton.setGeometry(QtCore.QRect(1890,0,30,25))
        self.exitButton.setObjectName("exitButton")

        icon = QIcon(str(IMAGES_DIR / "exitButton2.png"))
        self.exitButton.setIcon(icon)
        self.exitButton.setIconSize(QtCore.QSize(30,25))

        self.exitButton.setStyleSheet("background-color: transparent;")
        self.exitButton.clicked.connect(self.closeWindow)

        self.stackedWidget.addWidget(self.login)

        # create account page
        self.accountCreation = QtWidgets.QWidget()

        self.backgroundCreateAccount = QtWidgets.QLabel(self.accountCreation)
        self.backgroundCreateAccount.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.backgroundCreateAccount.setText("")
        self.backgroundCreateAccount.setPixmap(QtGui.QPixmap(str(IMAGES_DIR / "CreateAnAccount.png")))


        self.emailCreate = QtWidgets.QLineEdit(self.accountCreation)
        self.emailCreate.setGeometry(QtCore.QRect(699, 330, 523, 70))
        self.emailCreate.setStyleSheet("QLineEdit { background: rgba(0, 0, 0, 0); color: #CCCCCC; border: 1px solid transparent; }")
        self.emailCreate.setFont(QtGui.QFont("Montserrat Medium", 10))
        self.emailCreate.setMaxLength(255)

        self.usernameCreate = QtWidgets.QLineEdit(self.accountCreation)
        self.usernameCreate.setGeometry(QtCore.QRect(699, 410, 523, 70))
        self.usernameCreate.setStyleSheet("QLineEdit { background: rgba(0, 0, 0, 0); color: #CCCCCC; border: 1px solid transparent; }")
        self.usernameCreate.setFont(QtGui.QFont("Montserrat Medium", 10))
        self.usernameCreate.setMaxLength(15)

        self.passwordCreate = QtWidgets.QLineEdit(self.accountCreation)
        self.passwordCreate.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordCreate.setGeometry(QtCore.QRect(699, 489, 524, 70))
        self.passwordCreate.setStyleSheet("QLineEdit { background: rgba(0, 0, 0, 0); color: #CCCCCC; border: 1px solid transparent; }")
        self.passwordCreate.setFont(QtGui.QFont("Montserrat Medium", 10))
        self.passwordCreate.setMaxLength(15)

        self.createAnAccount = QtWidgets.QPushButton(self.accountCreation)
        self.createAnAccount.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.createAnAccount.setGeometry(QtCore.QRect(699, 567, 523, 39))
        self.createAnAccount.setText("Create an account")

        self.backButtonCreateAccount = QtWidgets.QPushButton(self.accountCreation)
        self.backButtonCreateAccount.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.backButtonCreateAccount.setGeometry(QtCore.QRect(30, 30, 60, 30))
        self.backButtonCreateAccount.setText("Back")

        self.backButtonCreateAccount.setIcon(QIcon(str(IMAGES_DIR / "Back_Arrow.png")))

        self.exitButtonCreateAccount= QtWidgets.QPushButton(self.accountCreation)
        self.exitButtonCreateAccount.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.exitButtonCreateAccount.setGeometry(QtCore.QRect(1890,0,30,25))
        self.exitButtonCreateAccount.setObjectName("exitButtonCreateAccount")

        self.exitButtonCreateAccount.setIcon(icon)
        self.exitButtonCreateAccount.setIconSize(QtCore.QSize(30,25))

        self.exitButtonCreateAccount.setStyleSheet("background-color: transparent;")
        self.exitButtonCreateAccount.clicked.connect(self.closeWindow)

        self.stackedWidget.addWidget(self.accountCreation)

        # forgot password page
        self.resetPassword = QtWidgets.QWidget()
        self.resetPassword.setObjectName("resetPassword")
        self.backgroundForgotPassword = QtWidgets.QLabel(self.resetPassword)
        self.backgroundForgotPassword.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.backgroundForgotPassword.setText("")
        self.backgroundForgotPassword.setPixmap(QtGui.QPixmap(str(IMAGES_DIR / "ForgotPassword.png")))

        self.emailForgot = QtWidgets.QLineEdit(self.resetPassword)
        self.emailForgot.setGeometry(QtCore.QRect(699, 330, 523, 70))
        self.emailForgot.setStyleSheet("QLineEdit { background: rgba(0, 0, 0, 0); color: #CCCCCC; border: 1px solid transparent; }")
        self.emailForgot.setFont(QtGui.QFont("Montserrat Medium", 10))

        self.newPassword = QtWidgets.QLineEdit(self.resetPassword)
        self.newPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.newPassword.setGeometry(QtCore.QRect(699, 410, 523, 70))
        self.newPassword.setStyleSheet("QLineEdit { background: rgba(0, 0, 0, 0); color: #CCCCCC; border: 1px solid transparent; }")
        self.newPassword.setFont(QtGui.QFont("Montserrat Medium", 10))
        self.newPassword.setMaxLength(15)

        self.resetPasswordForgotPassword = QtWidgets.QPushButton(self.resetPassword)
        self.resetPasswordForgotPassword.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.resetPasswordForgotPassword.setGeometry(QtCore.QRect(699, 490, 523, 39))
        self.resetPasswordForgotPassword.setText("Reset Password")

        self.backButtonForgotPassword = QtWidgets.QPushButton(self.resetPassword)
        self.backButtonForgotPassword.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.backButtonForgotPassword.setGeometry(QtCore.QRect(30, 30, 60, 30))
        self.backButtonForgotPassword.setText("Back")
        self.backButtonForgotPassword.setIcon(QIcon(str(IMAGES_DIR / "Back_Arrow.png")))

        self.exitButtonForgotPassword = QtWidgets.QPushButton(self.resetPassword)
        self.exitButtonForgotPassword.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.exitButtonForgotPassword.setGeometry(QtCore.QRect(1890,0,30,25))
        self.exitButtonForgotPassword.setObjectName("exitButtonForgotPassword")

        self.exitButtonForgotPassword.setIcon(icon)
        self.exitButtonForgotPassword.setIconSize(QtCore.QSize(30,25))

        self.exitButtonForgotPassword.setStyleSheet("background-color: transparent;")
        self.exitButtonForgotPassword.clicked.connect(self.closeWindow)


        self.stackedWidget.addWidget(self.resetPassword)

        # main page

        self.main = GraphVisualiser()

        self.stackedWidget.addWidget(self.main)


        self.homeButtonMain = QtWidgets.QPushButton(self.main)
        self.homeButtonMain.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.homeButtonMain.clicked.connect(self.backButtonPressed)

        self.homeButtonMain.setGeometry(QtCore.QRect(1860,0,30,25))
        self.homeButtonMain.setObjectName("homeButtonMain")

        self.homeButtonMain.setIcon(QIcon(str(IMAGES_DIR / "house2.png")))
        self.homeButtonMain.setIconSize(QtCore.QSize(30,25))
        self.homeButtonMain.setStyleSheet("background-color: transparent;")

        self.homeButtonMain.clicked.connect(self.backButtonPressed)

        self.exitButtonMain = QtWidgets.QPushButton(self.main)
        self.exitButtonMain.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.exitButtonMain.setGeometry(QtCore.QRect(1890,0,30,25))
        self.exitButtonMain.setObjectName("exitButtonMain")

        self.exitButtonMain.setIcon(icon)
        self.exitButtonMain.setIconSize(QtCore.QSize(30,25))
        self.exitButtonMain.setStyleSheet("background-color: transparent;")
        self.exitButtonMain.clicked.connect(self.closeWindow)



        MainWindow.setCentralWidget(self.centralwidget)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.forgotPassword.clicked.connect(self.switchToResetPasswordPage)
        self.createAnAccountLogin.clicked.connect(self.switchToCreateAccountPage)
        self.backButtonCreateAccount.clicked.connect(self.backButtonPressed)
        self.backButtonForgotPassword.clicked.connect(self.backButtonPressed)

    def closeWindow(self):
        raise SystemExit

    def switchToResetPasswordPage(self):
        self.stackedWidget.setCurrentIndex(2)

        self.clear_line()

    def switchToCreateAccountPage(self):
        self.stackedWidget.setCurrentIndex(1)

        self.clear_line()

    def backButtonPressed(self):
        self.stackedWidget.setCurrentIndex(0)

        self.clear_line()


    def clear_line(self):
        line_edits = [self.username, self.password, self.emailCreate, self.usernameCreate, self.passwordCreate, self.emailForgot, self.newPassword]
        for le in line_edits:
            le.clear()