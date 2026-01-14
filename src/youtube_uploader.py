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

    def upload_video(self, video_path, title, description, tags=None, privacy_status="private", publish_at=None):
        try:
            logger.info(f"Uploading video: {title}")
            
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags if tags else ['Psychology', 'Education', 'Mental Health'],
                    'categoryId': '27' # Education
                },
                'status': {
                    'privacyStatus': privacy_status if not publish_at else 'private',
                    'selfDeclaredMadeForKids': False,
                    'publishAt': publish_at # ISO 8601 format: YYYY-MM-DDThh:mm:ss.sZ
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

    def add_comment(self, video_id, text):
        """Adds a top-level comment to a video."""
        try:
            request = self.youtube.commentThreads().insert(
                part="snippet",
                body={
                    "snippet": {
                        "videoId": video_id,
                        "topLevelComment": {
                            "snippet": {
                                "textOriginal": text
                            }
                        }
                    }
                }
            )
            response = request.execute()
            comment_id = response['snippet']['topLevelComment']['id']
            logger.info(f"Comment added. ID: {comment_id}")
            return comment_id
        except Exception as e:
            logger.warning(f"Failed to add comment: {e}")
            return None

    def pin_comment(self, comment_id):
        """Pins a comment (requires high-level scope)."""
        try:
            request = self.youtube.comments().setAttributes(
                id=comment_id,
                part="snippet",
                body={
                    "snippet": {
                        "viewerRating": "none",
                        "isPinned": True
                    }
                }
            )
            request.execute()
            logger.info(f"Comment {comment_id} pinned.")
            return True
        except Exception as e:
            logger.warning(f"Failed to pin comment: {e} (This usually requires force-ssl scope)")
            return False

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
