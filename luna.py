import sys
import yt_dlp
import os
import ctypes

# Add VLC folder to PATH before importing vlc
vlc_path = r"C:\Program Files\VideoLAN\VLC"
if os.path.isdir(vlc_path):
    os.environ['PATH'] = vlc_path + os.pathsep + os.environ.get('PATH', '')

import vlc  # now import after PATH is fixed

def play_song(song_query):
    print(f"🔍 Searching for: {song_query}")

    # Load libvlc.dll explicitly (optional but safe)
    ctypes.CDLL(os.path.join(vlc_path, 'libvlc.dll'))

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch',
        'extract_flat': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(song_query, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            stream_url = info['url']
            title = info['title']
            print(f"🎵 Now Playing: {title}")

            player = vlc.MediaPlayer(stream_url)
            player.play()

            input("⏹ Press Enter to stop playback...\n")
            player.stop()

    except Exception as e:
        print("❌ Error:", str(e))

def main():
    if len(sys.argv) < 3 or sys.argv[1] != 'play':
        print("Usage: luna play <song name>")
        return

    song_query = ' '.join(sys.argv[2:])
    play_song(song_query)

if __name__ == '__main__':
    main()
