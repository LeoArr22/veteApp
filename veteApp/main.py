import sys
from PyQt5 import QtWidgets
from view.splash_controller import SplashScreen

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # Iniciamos el Splash
    splash = SplashScreen()
    splash.show()
    
    sys.exit(app.exec_())