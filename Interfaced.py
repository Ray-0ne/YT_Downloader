import tkinter as tk
from tkinter import messagebox, ttk
import yt_dlp
import threading

def create_progress_popup():
    popup = tk.Toplevel(root)
    popup.title("Downloading...")
    popup.geometry("420x140")
    popup.resizable(False, False)

    tk.Label(popup, text="Downloading video...").pack(pady=5)

    progress = ttk.Progressbar(popup, orient='horizontal', length=380, mode='determinate')
    progress.pack(pady=10)

    speed_label = tk.Label(popup, text="Progress: 0% - Speed: 0 KB/s", font=("Segoe UI", 10))
    speed_label.pack()

    return popup, progress, speed_label

def download_with_progress(url):
    try:
        popup, progress_bar, speed_label = create_progress_popup()

        def progress_hook(d):
            if d['status'] == 'downloading':
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes') or d.get('total_bytes_estimate') or 1
                percent = (downloaded / total) * 100
                speed = d.get('speed', 0)
                speed_kbps = speed / 1024 if speed else 0

                progress_bar['value'] = percent
                speed_label.config(
                    text=f"Progress: {percent:.1f}% - Speed: {speed_kbps:.1f} KB/s"
                )
                popup.update_idletasks()

            elif d['status'] == 'finished':
                progress_bar['value'] = 100
                speed_label.config(text="Download complete. Finalizing...")
                popup.update_idletasks()

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',# format alternate bestvideo[height<=1080][fps<=30][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]
                                                 #'bestvideo[height<=1080][fps<=30]+bestaudio/best
            'subtitleslangs': ['en'],
            'writesubtitles': True,
            'writeautomaticsub': True,
            'embedsubtitles': True,
            'merge_output_format': 'mp4',
            'outtmpl': '%(title)s.%(ext)s',
            'quiet': True,
            'progress_hooks': [progress_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        popup.destroy()
        messagebox.showinfo("Success", "Download completed!")

    except Exception as e:
        popup.destroy()
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

def on_download_click():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube video URL.")
        return

    download_button.config(state=tk.DISABLED)
    status_label.config(text="Starting download...")

    def threaded_download():
        download_with_progress(url)
        download_button.config(state=tk.NORMAL)
        status_label.config(text="")

    threading.Thread(target=threaded_download).start()

# -------------------- GUI SETUP --------------------

root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("500x200")
root.resizable(False, False)

# Header
tk.Label(root, text="YouTube Downloader with Subtitles", font=("Segoe UI", 14, "bold")).pack(pady=10)

# URL Entry
url_entry = ttk.Entry(root, width=60)
url_entry.pack(pady=5)
url_entry.focus()

# Download Button
download_button = ttk.Button(root, text="Download", command=on_download_click)
download_button.pack(pady=10)

# Status Label
status_label = tk.Label(root, text="", font=("Segoe UI", 10), fg="green")
status_label.pack()

# Run GUI
root.mainloop()
