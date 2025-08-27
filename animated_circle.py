import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QColor, QPen, QRadialGradient, QBrush, QPainterPath

class PlasmaSphere(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plasma Energy Sphere")
        self.setGeometry(100, 100, 600, 600)
        self.setStyleSheet("background-color: #000000;")
        
        self.time = 0
        self.streams = []
        for i in range(6):
            self.streams.append({
                'offset': i * 60,
                'speed': 1.5 + i * 0.2,
                'amplitude': 15 + i * 3
            })
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = 120
        
        # Multiple atmospheric glow layers
        for i, glow_radius in enumerate([350, 300, 250, 200]):
            alpha = 80 - i * 15
            intensity = (math.sin(math.radians(self.time + i * 30)) + 1) / 2
            glow_alpha = int(alpha * (0.7 + 0.3 * intensity))
            
            atm_glow = QRadialGradient(center_x, center_y, glow_radius)
            atm_glow.setColorAt(0, QColor(80 + int(40 * intensity), 120 + int(60 * intensity), 255, glow_alpha))
            atm_glow.setColorAt(0.6, QColor(40 + int(20 * intensity), 80 + int(40 * intensity), 200, glow_alpha // 2))
            atm_glow.setColorAt(1, QColor(0, 0, 0, 0))
            painter.setBrush(QBrush(atm_glow))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(center_x - glow_radius, center_y - glow_radius, glow_radius*2, glow_radius*2)
        
        # Black sphere center
        dark_sphere = QRadialGradient(center_x, center_y, radius)
        dark_sphere.setColorAt(0, QColor(0, 0, 0, 255))
        dark_sphere.setColorAt(0.8, QColor(10, 20, 40, 200))
        dark_sphere.setColorAt(1, QColor(20, 40, 80, 150))
        painter.setBrush(QBrush(dark_sphere))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center_x - radius, center_y - radius, radius*2, radius*2)
        
        # Flowing energy streams
        for stream in self.streams:
            path = QPainterPath()
            points = []
            
            for angle in range(0, 360, 5):
                t = self.time * stream['speed'] + stream['offset']
                wave_offset = stream['amplitude'] * math.sin(math.radians(angle * 3 + t))
                stream_radius = radius + 20 + wave_offset
                
                x = center_x + stream_radius * math.cos(math.radians(angle))
                y = center_y + stream_radius * math.sin(math.radians(angle))
                points.append((x, y))
            
            if points:
                path.moveTo(points[0][0], points[0][1])
                for i in range(1, len(points)):
                    path.lineTo(points[i][0], points[i][1])
                path.closeSubpath()
            
            # Blue to white color cycling
            intensity = (math.sin(math.radians(self.time * 2 + stream['offset'])) + 1) / 2
            blue_val = int(100 + 155 * intensity)
            white_val = int(200 + 55 * intensity)
            
            # Enhanced stream glow with atmospheric bleeding
            painter.setPen(QPen(QColor(30, 60, blue_val, 40), 15))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(path)
            
            painter.setPen(QPen(QColor(50, 100, blue_val, 100), 8))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(path)
            
            painter.setPen(QPen(QColor(white_val, white_val, 255, 220), 2))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(path)
        
        # Enhanced rim glow with pulsing
        pulse = (math.sin(math.radians(self.time * 3)) + 1) / 2
        rim_glow = QRadialGradient(center_x, center_y, radius + 20)
        rim_glow.setColorAt(0.8, QColor(0, 0, 0, 0))
        rim_glow.setColorAt(0.92, QColor(120 + int(60 * pulse), 180 + int(75 * pulse), 255, int(180 + 70 * pulse)))
        rim_glow.setColorAt(1, QColor(220 + int(35 * pulse), 240 + int(15 * pulse), 255, int(200 + 55 * pulse)))
        painter.setBrush(QBrush(rim_glow))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center_x - radius - 20, center_y - radius - 20, (radius + 20)*2, (radius + 20)*2)
    
    def update_animation(self):
        self.time = (self.time + 2) % 360
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlasmaSphere()
    window.show()
    sys.exit(app.exec_())