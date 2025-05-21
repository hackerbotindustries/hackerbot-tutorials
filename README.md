![HackerBot](images/transparent_hb_horizontal_industries_.png)
# 🤖 Hackerbot Tutorials

Welcome to the official **Hackerbot Tutorials** repository! This repo contains curated examples to help you get started with Hackerbot’s core features—including movement, vision, speech, and manipulation.

---

## 📆 Prerequisites

Before using these tutorials, make sure:

- You have a functional **Hackerbot** (AI / AI PRO / AI ELITE model)
- Firmware and software are fully **up to date**

---

## 🚀 Quick Start


### 👁️ Vision Setup

```bash
cd vision
pip3 install --no-cache-dir -r requirements.txt
```

Then run:

```bash
cd vision/image_rec
python3 yolo.py
```

or for face recognition:

```bash
cd vision/face_rec
python3 headshots_picam.py --name YourName --num_photos 10 --delay 2
python3 train_model.py
python3 facial_req.py
```

### 🗣️ Voice (Text to Speech)

1. Example usage in Python:
```python
bot.base.speak(model_src="en_GB-semaine-medium", text="Hello world", speaker_id=None)
```

## 🤾 Deploy AI in Hackerbot

1. Configure Gemini API key and put in the .env file

2. Run the example
```bash
cd AI
python3 speak_w_gemini.py
```

---

## ✅ Supported Models

| Feature             | AI Model | AI PRO | AI ELITE |
|---------------------|:--------:|:------:|:--------:|
| Base Movement       | ✅       | ✅     | ✅       |
| SLAM Navigation     | ✅       | ✅     | ✅       |
| Vision              | ✅       | ✅     | ✅       |
| Head Movement       | ❌       | ✅     | ✅       |
| Arm & Gripper       | ❌       | ❌     | ✅       |
| Text-to-Speech      | ✅       | ✅     | ✅       |

---

## 🧹 External Resources

- [Piper TTS models](https://github.com/rhasspy/piper)
- [Face Recognition on Raspberry Pi](https://core-electronics.com.au/guides/face-identify-raspberry-pi/)
- [Hailo AI Toolkit](https://docs.hailo.ai/)

---

## 🧹 Cleanup

When finished with any tutorial, destroy the bot instance to return to dock:

```python
bot.base.destroy(auto_dock=True)
```

---

## 🛠️ Contributions

Feel free to fork and extend with your own demos! Pull requests are welcome.

---

## 📄 License

MIT License

