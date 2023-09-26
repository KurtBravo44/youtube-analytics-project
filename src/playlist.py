from src.channel import youtube
import isodate
import datetime

class PlayList():

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.total = datetime.timedelta(0)
        self.most_liked = 0

        playlist_response = youtube.playlists().list(
            part='snippet',
            id=self.playlist_id
        ).execute()

        self.title = playlist_response['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'

        playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                               part='contentDetails',
                                               maxResults=50,
                                               ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        self.video_response = youtube.videos().list(part='contentDetails,statistics',
                                              id=','.join(video_ids)
                                              ).execute()

    @property
    def total_duration(self):
        for video in self.video_response['items']:

            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            self.total += duration
        return self.total

    def show_best_video(self):
        for video in self.video_response['items']:
            like_of_this_video = int(video['statistics']['likeCount'])
            if like_of_this_video > self.most_liked:
                self.most_liked = like_of_this_video

        for best_video in self.video_response['items']:
            if int(best_video['statistics']['likeCount']) == self.most_liked:
                return f'https://youtu.be/{best_video["id"]}'
