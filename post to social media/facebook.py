import sys
import requests
import json

# Facebook page ID and access token
facebook_page_id = "YOUR PAGE ID"
facebook_access_token = "YOUR ACCESS TOKEN"

def upload_media(page_id, image_file,job_description,access_token):
    """Upload an image to Facebook and return its media ID."""
    url = f"https://graph.facebook.com/v12.0/{page_id}/photos"
    params = {
        "access_token": access_token,
        "message": job_description
    }
    files = {
        "source": image_file  # expects file data in bytes
    }
    
    response = requests.post(url, params=params, files=files)
    if response.status_code == 200:
        print("Media uploaded successfully.")
        return response.json().get("id")
    else:
        print("Failed to upload media.")
        return None

def post_to_facebook(page_id, access_token, job_description, media_id=None):
    """Publishes a post on Facebook with optional media attachment."""
    url = f"https://graph.facebook.com/v12.0/{page_id}/feed"
    params = {
        "message": job_description,  # The description is included here
        "access_token": access_token
    }
    
    # If media_id is provided, attach it to the post
    if media_id:
        params["attached_media"] = json.dumps([{"media_fbid": media_id}])
    
    response = requests.post(url, data=params)
    
    # Debugging: print the response text and status code
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    
    if response.status_code == 200:
        print("Post published successfully.")
        return response.json()
    else:
        print(f"Failed to publish post: {response.text}")
        return None

# Command-line execution (optional for testing)
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No job description provided.")
        sys.exit(1)
    
    job_description = sys.argv[1]
    
    # Optionally handle image upload if image path is provided as a second argument
    media_id = None
    if len(sys.argv) > 2:
        image_path = sys.argv[2]
        with open(image_path, "rb") as image_file:
            media_id = upload_media(facebook_page_id, image_file,job_description,facebook_access_token)
    
    # Post to Facebook with the description and media ID (if available)
    post_to_facebook(facebook_page_id, facebook_access_token, job_description, media_id)
    print("Successfully posted to Facebook.")
