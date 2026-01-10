import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes required for the script
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def main():
    print("--- YouTube Refresh Token Generator ---")
    print("1. Ensure you have 'client_secrets.json' in this folder.")
    print("   (Download it from Google Cloud Console -> Credentials -> OAuth 2.0 Client IDs)")
    
    if not os.path.exists('client_secrets.json'):
        print("\n[ERROR] 'client_secrets.json' not found!")
        print("Please download your OAuth Client secret JSON file and rename it to 'client_secrets.json'.")
        return

    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secrets.json', SCOPES)
        creds = flow.run_local_server(port=0)
        
        print("\n[SUCCESS] Authentication successful!")
        print("Here is your Refresh Token (Save this as YOUTUBE_REFRESH_TOKEN in GitHub Secrets):")
        print("-" * 60)
        print(creds.refresh_token)
        print("-" * 60)
        
        # Also print Client ID and Secret just in case
        with open('client_secrets.json') as f:
            data = json.load(f)
            web = data.get('installed') or data.get('web')
            print(f"\nClient ID: {web.get('client_id')}")
            print(f"Client Secret: {web.get('client_secret')}")

    except Exception as e:
        print(f"\n[ERROR] Authentication failed: {e}")

if __name__ == "__main__":
    main()
