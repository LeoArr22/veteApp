import os
from PyQt5 import QtWidgets, uic, QtCore

class SplashScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        
        ui_path = os.path.join(os.path.dirname(__file__), 'splash.ui')
        uic.loadUi(ui_path, self) 
        
        self.setFixedSize(600, 400)
        
        # 1. Quitar bordes y fondo
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # 2. CENTRAR LA VENTANA
        self.centrar()

        # 3. Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.animar)
        self.timer.start(30)
        self.valor = 0

    def centrar(self):
        # Forzamos a que la ventana procese su tamaño real antes de moverla
        self.adjustSize() 
        
        # Obtenemos la pantalla principal
        pantalla = QtWidgets.QApplication.desktop().screenGeometry()
        
        # Obtenemos el tamaño de TU ventana (el splash)
        ventana = self.geometry()
        
        # Calculamos la posición x e y
        # (Ancho de pantalla - Ancho de ventana) / 2
        x = (pantalla.width() - ventana.width()) // 2
        y = (pantalla.height() - ventana.height()) // 2
        
        self.move(x, y)

    def animar(self):
        self.valor += 1
        if hasattr(self, 'barra_progreso'):
            self.barra_progreso.setValue(self.valor)
        
        if self.valor >= 100:
            self.timer.stop()
            self.close()