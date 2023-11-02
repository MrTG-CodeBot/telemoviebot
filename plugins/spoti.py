import pyrogram
from youtube_dl import YoutubeDL
import ffmpeg

class SpotifyDownloaderBot(pyrogram.Client):
    def __init__(self):
        super().__init__(config_file='config.env')

        # Set the default output audio format
        self.output_audio_format = 'mp3'

    def download_song(self, song_url):
        ydl = YoutubeDL()
        info = ydl.extract_info(song_url, download=False)

        # Check if the song URL is a playlist or album URL
        if info['extractor_key'] == 'SpotifyPlaylist':
            # Download all of the songs in the playlist
            for video in info['entries']:
                self.download_song(video['url'])
        elif info['extractor_key'] == 'SpotifyAlbum':
            # Download all of the songs in the album
            for track in info['tracks']:
                self.download_song(track['url'])
        else:
            # Download the single song
            video_path = ydl.download([song_url])

            # Convert the video to the specified audio format
            ffmpeg_input = ffmpeg.input(video_path)
            ffmpeg_output = ffmpeg_input.output(f'{info["title"]}.{self.output_audio_format}', audio_bitrate='320k')
            ffmpeg_output.run()

            # Send the audio file to the user
            self.send_audio(self.update.chat.id, f'{info["title"]}.{self.output_audio_format}', title=info["title"], artist=info["artist"])

    def search_songs(self, keyword):
        ydl = YoutubeDL()
        results = ydl.extract_info(f'ytsearch:{keyword}', download=False)

        # Return the first 10 results
        return results['entries'][:10]

    def on_message(self, message):
        if message.text.startswith('/search'):
            keyword = message.text.split(' ')[1]
            results = self.search_songs(keyword)

            # Send the results to the user
            for result in results:
                self.send_message(self.update.chat.id, f'[{result["title"]}]({result["url"]})')
        elif message.text.startswith('/format'):
            audio_format = message.text.split(' ')[1]

            # Validate the audio format
            if audio_format not in ['mp3', 'aac', 'flac']:
                self.send_message(self.update.chat.id, 'Invalid audio format.')
                return

            # Set the output audio format
            self.output_audio_format = audio_format
        elif message.text.startswith('/download'):
            song_url = message.text.split(' ')[1]
            self.download_song(song_url)

