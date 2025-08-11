import sys
import yt_dlp
import os
import ctypes
import json
import vlc
import threading
import time
import platform
import winreg

# Function to add your script folder to user PATH environment variable (Windows only)
def add_self_to_path():
    if platform.system() != "Windows":
        return
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_READ) as key:
            current_path, _ = winreg.QueryValueEx(key, "PATH")
    except FileNotFoundError:
        current_path = ""

    # Check if already in PATH (case insensitive)
    if script_dir.lower() in current_path.lower():
        return  # Already added

    new_path = script_dir + os.pathsep + current_path if current_path else script_dir
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_WRITE) as key:
            winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
        print(f"✅ Added {script_dir} to user PATH environment variable.")
        print("ℹ️ Please restart your command prompt or computer to use 'luna' from any directory.")
        # Update current process environment variable so subprocesses work now
        os.environ["PATH"] = new_path
    except Exception as e:
        print(f"❌ Failed to add to PATH: {e}")

# Call the function on startup
add_self_to_path()

# VLC Setup
vlc_path = r"C:\Program Files\VideoLAN\VLC"
if os.path.isdir(vlc_path):
    os.environ['PATH'] = vlc_path + os.pathsep + os.environ.get('PATH', '')
    try:
        ctypes.CDLL(os.path.join(vlc_path, 'libvlc.dll'))
    except Exception as e:
        print(f"❌ Failed loading VLC DLL: {e}")

# Paths for storage
DATA_DIR = os.path.join(os.path.expanduser("~"), ".luna_data")
FAV_FILE = os.path.join(DATA_DIR, "favorites.json")
PLAYLIST_DIR = os.path.join(DATA_DIR, "playlists")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLAYLIST_DIR, exist_ok=True)

player = None
stop_flag = False


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def search_youtube(song_query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch',
        'extract_flat': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(song_query, download=False)
        if 'entries' in info:
            info = info['entries'][0]
        return {
            'url': info['url'],
            'title': info['title'],
            'webpage_url': info.get('webpage_url', '')
        }


def play_stream(song_query, autoplay=True):
    global player, stop_flag
    stop_flag = False

    info = search_youtube(song_query)
    print(f"🎵 Now Playing: {info['title']}")
    print("⏹ Press ENTER to stop playback.")

    player = vlc.MediaPlayer(info['url'])
    player.play()

    def monitor():
        global player
        time.sleep(1)
        while player.is_playing():
            if stop_flag:
                player.stop()
                return
            time.sleep(1)
        if autoplay and not stop_flag:
            play_stream(info['title'])

    threading.Thread(target=monitor, daemon=True).start()

    # Wait for user input to stop
    input()
    stop_playback()


def stop_playback():
    global player, stop_flag
    stop_flag = True
    if player:
        player.stop()
    print("⏹ Playback stopped.")


def add_to_favorites(song_query):
    favs = load_json(FAV_FILE)
    favs.append(song_query)
    save_json(FAV_FILE, favs)
    print(f"⭐ Added to favorites: {song_query}")


def show_favorites():
    favs = load_json(FAV_FILE)
    if not favs:
        print("📭 No favorites yet.")
        return
    for i, song in enumerate(favs, 1):
        print(f"{i}. {song}")


def create_playlist(name):
    path = os.path.join(PLAYLIST_DIR, f"{name}.json")
    if os.path.exists(path):
        print(f"⚠️ Playlist '{name}' already exists.")
        return
    save_json(path, [])
    print(f"📁 Created playlist: {name}")


def add_to_playlist(song, playlist):
    path = os.path.join(PLAYLIST_DIR, f"{playlist}.json")
    if not os.path.exists(path):
        print(f"❌ Playlist '{playlist}' does not exist.")
        return
    songs = load_json(path)
    songs.append(song)
    save_json(path, songs)
    print(f"➕ Added to '{playlist}': {song}")


def play_playlist(name):
    path = os.path.join(PLAYLIST_DIR, f"{name}.json")
    if not os.path.exists(path):
        print(f"❌ Playlist '{name}' not found.")
        return
    songs = load_json(path)
    if not songs:
        print(f"📭 Playlist '{name}' is empty.")
        return

    def play_next(index):
        if index >= len(songs) or stop_flag:
            return
        play_stream(songs[index], autoplay=False)
        while player and player.is_playing():
            time.sleep(1)
        play_next(index + 1)

    threading.Thread(target=play_next, args=(0,), daemon=True).start()


def main():
    if len(sys.argv) < 2:
        print("Usage:\n"
              "  luna <song name>\n"
              "  luna stop\n"
              "  luna addfav <song>\n"
              "  luna favorite\n"
              "  luna create <playlist>\n"
              "  luna add <song> <playlist>\n"
              "  luna <playlist>")
        return

    cmd = sys.argv[1].lower()

    if cmd == "stop":
        stop_playback()
    elif cmd == "addfav" and len(sys.argv) > 2:
        song = ' '.join(sys.argv[2:])
        add_to_favorites(song)
    elif cmd == "favorite":
        show_favorites()
    elif cmd == "create" and len(sys.argv) > 2:
        create_playlist(sys.argv[2])
    elif cmd == "add" and len(sys.argv) > 3:
        song = sys.argv[2]
        playlist = sys.argv[3]
        add_to_playlist(song, playlist)
    else:
        query = ' '.join(sys.argv[1:])
        playlist_path = os.path.join(PLAYLIST_DIR, f"{query}.json")
        if os.path.exists(playlist_path):
            play_playlist(query)
        else:
            play_stream(query)


if __name__ == '__main__':
    main()
