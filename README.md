# 🤖 Twilight AI Voice Assistant

A animated robot voice assistant with PyQt5 GUI that responds to voice commands and performs various tasks.

## ✨ Features

### 🎨 Animated Robot GUI

- Custom-drawn robot with oval body, antenna, and pixelated face
- Real-time animations: blinking eyes, bobbing antenna, animated mouth
- Visual states: listening, processing, and idle modes
- Black background with green glowing elements

### 🎤 Voice Commands

- **Basic Interaction**: "twilight", "hello", "who are you", "how are you"
- **Web Navigation**: Open YouTube, Google, GitHub, Spotify, Netflix, Amazon, Notion, TradingView, Chess.com, LinkedIn, WhatsApp, Anime (HiAnime), Gemini
- **YouTube Features**: Search and play specific content
- **Utilities**: Current time, screenshots, AI responses
- **Exit**: "bye", "exit", "thank you"

### 🧠 AI Integration

- Powered by Groq API with Llama3-8b model
- Natural conversation capabilities
- Concise responses under 100 words

## 🚀 Quick Start

### Prerequisites

```bash
pip install PyQt5 SpeechRecognition requests pyaudio
```

### Installation

1. Clone or download the repository
2. Install dependencies
3. **Configure API Key** (Required for AI responses):
   - Open `main_cute_robot.py`
   - Find line 130 and replace with your Groq API key:
   ```python
   "Authorization": "Bearer YOUR_GROQ_API_KEY_HERE"
   ```
   - Get your free API key from: https://console.groq.com/
4. Run the application:

```bash
python main_cute_robot.py
```

## 📁 Project Structure

```
Twilight/
├── main_cute_robot.py    # Main animated GUI application
├── main_simple.py        # Console-only version
├── main.py              # Original full-featured version
├── screenshots/         # Auto-generated screenshots
└── README.md           # This file
```

## 🎯 Voice Commands Reference

| Command                    | Action                |
| -------------------------- | --------------------- |
| `"twilight"`               | Acknowledge command   |
| `"hello"`                  | Greet user            |
| `"how are you"`            | Ask about status      |
| `"open youtube"`           | Open YouTube          |
| `"search youtube [query]"` | Search YouTube        |
| `"play [song/artist]"`     | Play music on YouTube |
| `"play"`                   | Play default music    |
| `"open google"`            | Open Google           |
| `"open anime"`             | Open HiAnime          |
| `"open gemini"`            | Open Google Gemini    |
| `"open github"`            | Open GitHub           |
| `"open spotify"`           | Open Spotify          |
| `"open netflix"`           | Open Netflix          |
| `"open amazon"`            | Open Amazon           |
| `"open notion"`            | Open Notion           |
| `"open tradingview"`       | Open TradingView      |
| `"open chess"`             | Open Chess.com        |
| `"open linkedin"`          | Open LinkedIn         |
| `"open whatsapp"`          | Open WhatsApp Web     |
| `"current time"`           | Tell current time     |
| `"take screenshot"`        | Capture screen        |
| `"who are you"`            | Robot introduction    |
| `"thank you"`              | Polite response       |
| `"bye"` / `"exit"`         | Close application     |

## 🛠️ Technical Details

### Dependencies

- **PyQt5**: GUI framework and animations
- **SpeechRecognition**: Voice input processing
- **Requests**: API communications
- **Threading**: Concurrent voice processing
- **Webbrowser**: URL opening
- **Subprocess**: System integrations

### Animation System

- 200ms refresh rate for smooth animations
- Sine wave calculations for natural movement
- State-based visual feedback
- Blinking cycle every 3 seconds

### Voice Processing

- Google Speech Recognition API
- Ambient noise adjustment
- Timeout handling for continuous listening
- PowerShell TTS for speech output

## 🎨 Customization

### Robot Appearance

Modify `CuteRobotWidget.paintEvent()` to change:

- Colors and sizes
- Animation patterns
- Visual states

### Voice Commands

Add new commands in `voice_assistant()` function:

```python
elif "your command" in command:
    speak("Your response")
    # Your action here
```

### Animation Speed

Adjust timer interval in `CuteRobotGUI.__init__()`:

```python
self.animation_timer.start(200)  # milliseconds
```

## 🔧 Troubleshooting

### Common Issues

- **Microphone not working**: Check system permissions and microphone settings
- **Speech not clear**: Adjust microphone sensitivity in Windows
- **GUI not showing**: Ensure PyQt5 is properly installed (`pip install PyQt5`)
- **Voice commands not recognized**: Speak clearly and check internet connection
- **AI responses not working**: Verify Groq API key is correctly configured
- **"Authorization failed"**: Check if API key is valid and has credits

### System Requirements

- Windows 10/11 (for PowerShell TTS)
- Microphone access
- Internet connection
- Python 3.7+
- **Groq API Key** (free at https://console.groq.com/)

## ⚙️ Configuration

### API Setup

1. **Groq API Key**: Required for AI responses
   - Sign up at https://console.groq.com/
   - Generate a free API key
   - Replace the existing key in `main_cute_robot.py` line 130

### Audio Setup

- Ensure microphone permissions are enabled
- Test microphone in Windows settings
- Speak clearly for better recognition

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to fork, modify, and submit pull requests. All contributions are welcome!

## 🌟 Acknowledgments

- Groq API for AI responses
- Google Speech Recognition
- PyQt5 community
- Open source contributors