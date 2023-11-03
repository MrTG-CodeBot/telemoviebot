import pyrogram.client as pyrogram
from youtube_dl import YoutubeDL
import ffmpeg
from info import API_ID, API_HASH, BOT_TOKEN

class MusicBot(pyrogram.Client):

    # Set the default output audio format
    output_audio_format = 'mp3'

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
            try:
                video_path = ydl.download([song_url])

                # Convert the video to the specified audio format
                ffmpeg_input = ffmpeg.input(video_path)
                ffmpeg_output = ffmpeg_input.output(f'{info["title"]}.{self.output_audio_format}', audio_bitrate='320k')
                ffmpeg_output.run()

                # Send the audio file to the user
                self.client.send_document(self.update.chat.id, f'{info["title"]}.{self.output_audio_format}', caption=f'{info["title"]} by {info["artist"]}')
            except Exception as e:
                self.client.send_message(self.update.chat.id, f'An error occurred while downloading the song: {e}')

    def search_songs(self, keyword):
        ydl = YoutubeDL()
        results = ydl.extract_info(f'ytsearch:{keyword}', download=False)

        # Return the first 10 results
        return results['entries'][:10]

    def on_message(self, message):
        if message.text.startswith('/song'):
            keyword = message.text.split(' ')[1]
            results = self.search_songs(keyword)

            # Send the results to the user
            for result in results:
                self.client.send_message(self.update.chat.id, f'[{result
