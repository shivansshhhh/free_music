# 🎧 Luna — YouTube Music Player via Command Line using VLC (Free Music ads free)

Luna is a lightweight command-line tool that lets you stream music directly from YouTube using simple search commands — powered by `yt_dlp` and `VLC`.

> 🔊 Example:  
> ```bash
> python luna.py play shape of you
> ```

---

## ✨ Features

- 🎵 Search and play any song from YouTube via command line
- ⚡ Streams audio without downloading
- 🧠 Uses `yt_dlp` for smart searching
- 🎮 Uses `VLC` for smooth audio playback

---

## 💻 Requirements

- **Python 3.7+** (must be 64-bit)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [VLC Media Player (64-bit)](https://www.videolan.org/vlc/)

---

## 📦 Installation

### 1. Install Python dependencies

```bash
pip install yt-dlp python-vlc
```
### 2. Install VLC (64-bit)
    Download from https://www.videolan.org/vlc/
Must be installed to:

    C:\Program Files\VideoLAN\VLC
### 🚀 Usage
Run the script with the following format:

    python luna.py play <song name>
Example:

    python luna.py play shape of you
You'll see:

    🔍 Searching for: shape of you
    🎵 Now Playing: Ed Sheeran - Shape of You [Official Video]
    ⏹ Press Enter to stop playback...
    
### 🛠 Configuration
If your VLC install path is different, modify this line in luna.py:

    vlc_path = r"C:\Program Files\VideoLAN\VLC"
    Make sure libvlc.dll is located inside that folder.

### 🐚 CMD Shell Version for Win
For a more interactive shell experience (like luna > play shape of you), check the companion repo:

    Download luna.exe open it.
    Download VLC player 64bit install it.
    set path inside encvironment variables of where your luna.exe located.
    open shell or cmd type- "luna <song name>.
    enjoy song.

### 📃 License
MIT License

### 🙏 Credits

    yt-dlp

    python-vlc

    VLC

---

    Python such a greate language, with community and libraries are much easy to find.

---

