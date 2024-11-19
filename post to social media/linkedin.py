import sys
import requests
import json
import os

# LinkedIn access token and user URN
linkedin_access_token = "YOUR ACCESS TOKEN"
person_urn = "YOUR PERSON URN"

def get_upload_url(access_token):
    """Request an upload URL for the image."""
    api_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "registerUploadRequest": {
            "owner": person_urn,
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "serviceRelationships": [{
                "relationshipType": "OWNER",
                "identifier": "urn:li:userGeneratedContent"
            }]
        }
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        upload_data = response.json()
        upload_url = upload_data["value"]["uploadMechanism"]["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]["uploadUrl"]
        asset_urn = upload_data["value"]["asset"]
        return upload_url, asset_urn
    else:
        print("Failed to get upload URL.")
        return None, None

def upload_image(upload_url, image_path):
    """Upload an image to LinkedIn using the provided upload URL."""
    headers = {
        "Authorization": f"Bearer {linkedin_access_token}",
        "Content-Type": "image/jpeg"
    }
    with open(image_path, "rb") as image_file:
        response = requests.put(upload_url, headers=headers, data=image_file)
    if response.status_code == 201:
        print("Image uploaded successfully.")
        return True
    else:
        print("Failed to upload image.")
        return False

def post_to_linkedin(access_token, person_urn, job_description, asset_urn=None):
    """Post a job description to LinkedIn, optionally with an image."""
    api_url = 'https://api.linkedin.com/v2/ugcPosts'
    media = [{"status": "READY", "media": asset_urn}] if asset_urn else []
    payload = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": job_description
                },
                "shareMediaCategory": "IMAGE" if media else "NONE",
                "media": media
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    response = requests.post(api_url, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        print("Job posted to LinkedIn successfully.")
    else:
        print(f"Failed to post job to LinkedIn: {response.text}")

# Command-line usage (optional if you want to test this directly)
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python linkedin.py <job_description> <image_path>")
        sys.exit(1)
    
    # Retrieve job description and image path from command line arguments
    job_description = sys.argv[1]
    image_path = sys.argv[2]

    # Get upload URL and asset URN for the image
    upload_url, asset_urn = get_upload_url(linkedin_access_token)
    
    # Upload image if a path is provided
    if image_path and os.path.exists(image_path):
        if upload_url:
            if upload_image(upload_url, image_path):
                post_to_linkedin(linkedin_access_token, person_urn, job_description, asset_urn)
        else:
            print("Image upload failed due to no upload URL.")
    else:
        post_to_linkedin(linkedin_access_token, person_urn, job_description)
    print("Successfully posted to LinkedIn.")
