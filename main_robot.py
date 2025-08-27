import sys
import speech_recognition as sr
import webbrowser
import os  
import requests
import json
from datetime import datetime
import threading
import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont, QRadialGradient, QPainterPath
from PyQt5.QtCore import QRect

recognizer = sr.Recognizer()

class SignalEmitter(QObject):
    status_changed = pyqtSignal(str)

class PlasmaSphereWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.listening = False
        self.processing = False
        self.time = 0
        # No streams needed for geometric rings
        pass
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = 80
        
        # Adjust intensity based on state
        base_intensity = 1.0
        if self.listening:
            base_intensity = 1.5
        elif self.processing:
            base_intensity = 1.2
        
        # Enhanced atmospheric glow layers
        for i, glow_radius in enumerate([300, 250, 200, 170, 140, 120]):
            alpha = int((80 - i * 8) * base_intensity)
            intensity = (math.sin(math.radians(self.time + i * 30)) + 1) / 2
            glow_alpha = int(alpha * (0.6 + 0.4 * intensity))
            
            atm_glow = QRadialGradient(center_x, center_y, glow_radius)
            atm_glow.setColorAt(0, QColor(int(90 * base_intensity + 50 * intensity), int(140 * base_intensity + 70 * intensity), 255, glow_alpha))
            atm_glow.setColorAt(0.5, QColor(int(60 * base_intensity + 30 * intensity), int(100 * base_intensity + 50 * intensity), 220, glow_alpha // 2))
            atm_glow.setColorAt(0.8, QColor(int(30 * base_intensity + 15 * intensity), int(60 * base_intensity + 30 * intensity), 180, glow_alpha // 4))
            atm_glow.setColorAt(1, QColor(0, 0, 0, 0))
            painter.setBrush(QBrush(atm_glow))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(center_x - glow_radius, center_y - glow_radius, glow_radius*2, glow_radius*2)
        
        # Black sphere center
        dark_sphere = QRadialGradient(center_x, center_y, radius)
        dark_sphere.setColorAt(0, QColor(0, 0, 0, 255))
        dark_sphere.setColorAt(0.8, QColor(int(10 * base_intensity), int(20 * base_intensity), int(40 * base_intensity), 200))
        dark_sphere.setColorAt(1, QColor(int(20 * base_intensity), int(40 * base_intensity), int(80 * base_intensity), 150))
        painter.setBrush(QBrush(dark_sphere))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center_x - radius, center_y - radius, radius*2, radius*2)
        
        # Geometric interlocking rings
        ring_radius = radius + 30
        
        # Draw multiple interlocking rings
        for i in range(8):
            angle_offset = i * 22.5  # 360/16 for even distribution
            rotation = self.time * 0.5 + angle_offset
            
            # Create tilted ellipse for 3D effect
            path = QPainterPath()
            points = []
            
            for angle in range(0, 360, 3):
                # Create elliptical ring with rotation
                rad = math.radians(angle)
                x_base = ring_radius * math.cos(rad)
                y_base = ring_radius * 0.3 * math.sin(rad)  # Flattened for 3D look
                
                # Rotate the ring
                rot_rad = math.radians(rotation)
                x = center_x + x_base * math.cos(rot_rad) - y_base * math.sin(rot_rad)
                y = center_y + x_base * math.sin(rot_rad) + y_base * math.cos(rot_rad)
                points.append((x, y))
            
            if points:
                path.moveTo(points[0][0], points[0][1])
                for j in range(1, len(points)):
                    path.lineTo(points[j][0], points[j][1])
                path.closeSubpath()
            
            # Color based on ring position
            intensity = (math.sin(math.radians(self.time + i * 45)) + 1) / 2
            alpha = int((100 + 100 * intensity) * base_intensity)
            
            # Draw glowing ring
            painter.setPen(QPen(QColor(80, 150, 255, alpha // 3), 8))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(path)
            
            painter.setPen(QPen(QColor(150, 200, 255, alpha), 3))
            painter.setBrush(Qt.NoBrush)
            painter.drawPath(path)
        
        # Enhanced rim glow with pulsing
        pulse = (math.sin(math.radians(self.time * 3)) + 1) / 2 * base_intensity
        rim_glow = QRadialGradient(center_x, center_y, radius + 15)
        rim_glow.setColorAt(0.8, QColor(0, 0, 0, 0))
        rim_glow.setColorAt(0.92, QColor(int(120 + 60 * pulse), int(180 + 75 * pulse), 255, int(180 + 70 * pulse)))
        rim_glow.setColorAt(1, QColor(int(220 + 35 * pulse), int(240 + 15 * pulse), 255, int(200 + 55 * pulse)))
        painter.setBrush(QBrush(rim_glow))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(center_x - radius - 15, center_y - radius - 15, (radius + 15)*2, (radius + 15)*2)

class TwilightGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.signals = SignalEmitter()
        self.signals.status_changed.connect(self.update_status)
        self.running = True
        
        self.setWindowTitle("Twilight AI")
        self.setGeometry(300, 300, 500, 500)
        self.setStyleSheet("background-color: #000000;")
        
        self.sphere_widget = PlasmaSphereWidget()
        self.setCentralWidget(self.sphere_widget)
        
        # Animation timer
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate_sphere)
        self.animation_timer.start(80)
        
    def animate_sphere(self):
        self.sphere_widget.time = (self.sphere_widget.time + 1) % 360
        self.sphere_widget.update()
        
    def update_status(self, text):
        self.sphere_widget.listening = "listening" in text.lower()
        self.sphere_widget.processing = "processing" in text.lower()
    
    def closeEvent(self, event):
        self.running = False
        event.accept()

def currentTime():
    now = datetime.now()
    time_str = now.strftime("%I:%M %p")
    return f"The current time is {time_str}"

def get_ai_response(question):
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": "Bearer ENTER_YOUR_API_KEY_HERE",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are Twilight, a helpful robot assistant. Keep responses concise and under 100 words."},
                {"role": "user", "content": question}
            ],
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return "I'm here to help you with various tasks and questions."
            
    except Exception as e:
        return "I'm here to help you with various tasks and questions."

def take_screenshot():
    try:
        import subprocess
        screenshots_dir = os.path.join(os.getcwd(), "screenshots")
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(screenshots_dir, filename)
        
        ps_script = f'''Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds; $bitmap = New-Object System.Drawing.Bitmap $screen.Width, $screen.Height; $graphics = [System.Drawing.Graphics]::FromImage($bitmap); $graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size); $bitmap.Save("{filepath}"); $graphics.Dispose(); $bitmap.Dispose()'''
        
        subprocess.run(['powershell', '-Command', ps_script], check=True, capture_output=True)
        
        return filepath, filename
    except Exception as e:
        return None, None

def speak(text):
    try:
        import subprocess
        clean_text = ''.join(c for c in text if c.isalnum() or c.isspace())
        clean_text = ' '.join(clean_text.split())
        
        cmd = ['powershell', '-Command', f'Add-Type -AssemblyName System.Speech; (New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak("{clean_text}")']
        subprocess.run(cmd, check=True, capture_output=True)
    except Exception as e:
        pass

def voice_assistant(gui):
    speak("Initializing twilight")
    gui.signals.status_changed.emit("Ready")
    
    while gui.running:
        try:
            with sr.Microphone() as source:
                gui.signals.status_changed.emit("Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio = recognizer.listen(source, timeout=1)
                gui.signals.status_changed.emit("Processing...")
                command = recognizer.recognize_google(audio).lower()
                
                if "twilight" in command:
                    speak("Yes")
                elif "search youtube" in command or "youtube search" in command or "search on youtube" in command:
                    # Extract search term more carefully
                    search_term = command
                    for phrase in ["search youtube for", "search youtube", "youtube search for", "youtube search", "search on youtube for", "search on youtube"]:
                        search_term = search_term.replace(phrase, "")
                    search_term = search_term.strip()
                    
                    if search_term:
                        speak(f"Searching YouTube for {search_term}")
                        search_url = f"https://www.youtube.com/results?search_query={search_term.replace(' ', '+')}"
                        webbrowser.open(search_url)
                    else:
                        speak("What to search?")
                elif "open google" in command:
                    speak("Opening Google")
                    webbrowser.open("https://www.google.com")
                elif "open anime" in command:
                    speak("Opening anime")
                    webbrowser.open("https://hianime.nz")
                elif "open gemini" in command:
                    speak("Opening Gemini")
                    webbrowser.open("https://gemini.google.com")
                elif "open github" in command:
                    speak("Opening GitHub")
                    webbrowser.open("https://github.com/Mrutyunjaypathe")
                elif "current time" in command or "what time is it" in command or "time" in command:
                    current_time = currentTime()
                    speak(current_time)
                elif "open spotify" in command:
                    speak("Opening Spotify")
                    webbrowser.open("https://www.spotify.com")
                elif "open netflix" in command:
                    speak("Opening Netflix")
                    webbrowser.open("https://www.netflix.com")
                elif "open amazon" in command:
                    speak("Opening Amazon")
                    webbrowser.open("https://www.amazon.com")
                elif "open notion" in command:
                    speak("Opening Notion")
                    webbrowser.open("https://www.notion.so")
                elif "open tradingview" in command:
                    speak("Opening TradingView")
                    webbrowser.open("https://in.tradingview.com")
                elif "open chess" in command:
                    speak("Opening Chess")
                    webbrowser.open("https://www.chess.com")
                elif "open linkedin" in command:
                    speak("Opening LinkedIn")
                    webbrowser.open("https://www.linkedin.com")
                elif "open whatsapp" in command:
                    speak("Opening WhatsApp")
                    webbrowser.open("https://web.whatsapp.com")
                elif "take screenshot" in command or "screenshot" in command:
                    speak("Taking screenshot")
                    filepath, filename = take_screenshot()
                    if filepath:
                        speak("Screenshot saved")
                    else:
                        speak("Screenshot failed")
                elif "play my music" in command:
                    speak("Playing music")
                    webbrowser.open("https://www.youtube.com/watch?v=XlOBtQSjYRU&list=RDXlOBtQSjYRU&start_radio=1")
                elif "who are you" in command:
                    speak("I am Twilight robot")
                elif "how are you" in command:
                    speak("I am fine, thank you")
                elif "open" in command and command != "open":
                    # Extract what to open more carefully
                    open_query = command
                    for phrase in ["open on youtube", "open"]:
                        open_query = open_query.replace(phrase, "")
                    open_query = open_query.strip()
                    if open_query:
                        speak(f"Opening {open_query}")
                        search_url = f"https://www.youtube.com/results?search_query={open_query.replace(' ', '+')}"
                        webbrowser.open(search_url)
                elif command == "open":
                    speak("Opening music")
                    webbrowser.open("https://www.youtube.com/watch?v=XlOBtQSjYRU&list=RDXlOBtQSjYRU&start_radio=1")

                elif "thank you" in command:
                    speak("You're welcome")
                elif "bye" in command or "exit" in command:
                    speak("Goodbye")
                    gui.close()
                    return
                else:
                    ai_response = get_ai_response(command)
                    speak(ai_response)
                
                gui.signals.status_changed.emit("Ready")
                
        except sr.UnknownValueError:
            gui.signals.status_changed.emit("Ready")
        except sr.RequestError:
            gui.signals.status_changed.emit("Ready")
        except sr.WaitTimeoutError:
            pass
        except Exception:
            gui.signals.status_changed.emit("Ready")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = TwilightGUI()
    gui.show()
    
    voice_thread = threading.Thread(target=voice_assistant, args=(gui,), daemon=True)
    voice_thread.start()
    
    sys.exit(app.exec_())