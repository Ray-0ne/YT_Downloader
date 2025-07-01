import yt_dlp

def download_video(url):
    options = {
        'format': 'bestvideo+bestaudio/best',  # High quality video + audio
        'subtitleslangs': ['en'],              # Choose subtitle language (e.g., 'en' for English)
        'writesubtitles': True,                # Download subtitles
        'writeautomaticsub': True,             # Download auto-generated subtitles if necessary
        'embedsubtitles': True,                # Embed subtitles into the video
        'outtmpl': '%(title)s.%(ext)s',        # Save with video title
        'merge_output_format': 'mp4',          # Final format
        'quiet': False                         # Show progress
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    download_video(video_url)
