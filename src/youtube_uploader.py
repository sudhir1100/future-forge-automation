import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from src.config import Config
import logging

logger = logging.getLogger(__name__)

class YouTubeUploader:
    def __init__(self):
        self.youtube = self._get_authenticated_service()

    def _get_authenticated_service(self):
        try:
            credentials = google.oauth2.credentials.Credentials(
                None, # No access token initially
                refresh_token=Config.YOUTUBE_REFRESH_TOKEN,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=Config.YOUTUBE_CLIENT_ID,
                client_secret=Config.YOUTUBE_CLIENT_SECRET
            )
            return build("youtube", "v3", credentials=credentials)
        except Exception as e:
            logger.error(f"Failed to authenticate with YouTube: {e}")
            raise

    def upload_video(self, video_path, title, description, privacy_status="private"):
        try:
            logger.info(f"Uploading video: {title}")
            
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': ['Psychology', 'Human Behavior', 'Mental Health', 'Deep Secrets', 'Archetypes', 'Healing'],
                    'categoryId': '27' # Education
                },
                'status': {
                    'privacyStatus': privacy_status,
                    'selfDeclaredMadeForKids': False
                }
            }

            # MediaFileUpload handles the file upload
            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

            request = self.youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )

            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    logger.info(f"Uploaded {int(status.progress() * 100)}%")

            logger.info(f"Upload Complete! Video ID: {response['id']}")
            return response['id']

        except Exception as e:
            logger.error(f"Failed to upload video: {e}")
            return None
    def set_thumbnail(self, video_id, thumbnail_path):
        """Uploads a custom thumbnail for a video."""
        try:
            logger.info(f"Uploading thumbnail for {video_id}...")
            if not os.path.exists(thumbnail_path):
                logger.error(f"Thumbnail file not found: {thumbnail_path}")
                return False

            request = self.youtube.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(thumbnail_path)
            )
            response = request.execute()
            logger.info("Thumbnail uploaded successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to upload thumbnail: {e}")
            return False
