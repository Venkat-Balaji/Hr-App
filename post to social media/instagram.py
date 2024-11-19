import sys
import requests
import boto3
import os

# Instagram API credentials
access_token = "YOUR ACCESS TOKEN"
instagram_account_id = "YOUR ACCOUNT ID"

# AWS S3 credentials
aws_access_key = "YOUR AWS ACCESS TOKEN"
aws_secret_key = "YOUR  SECRET KEY"
aws_bucket_name = "YOUR BUCKET NAME"

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name='us-east-1'
)

# Function to upload image to S3
def upload_image_to_s3(file_path, bucket_name, object_key):
    try:
        with open(file_path, "rb") as file:
            s3_client.upload_fileobj(file, bucket_name, object_key, ExtraArgs={'ACL': 'public-read'})
        return True
    except Exception as e:
        print(f"Error uploading image to S3: {e}")
        return False

# Function to generate public URL for image in S3
def get_image_url(bucket_name, object_key):
    return f"https://{bucket_name}.s3.{s3_client.meta.region_name}.amazonaws.com/{object_key}"

# Function to post to Instagram
def post_to_instagram(image_url, caption):
    create_media_url = f"https://graph.facebook.com/v17.0/{instagram_account_id}/media"
    payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": access_token
    }

    response = requests.post(create_media_url, data=payload)
    if response.status_code == 200:
        media_id = response.json().get("id")
        if media_id:
            publish_url = f"https://graph.facebook.com/v17.0/{instagram_account_id}/media_publish"
            publish_payload = {
                "creation_id": media_id,
                "access_token": access_token
            }
            publish_response = requests.post(publish_url, data=publish_payload)
            if publish_response.status_code == 200:
                print("Image posted successfully on Instagram!")
                return True
            else:
                print(f"Failed to publish the media on Instagram: {publish_response.json()}")
        else:
            print("Failed to create media object on Instagram.")
    else:
        print(f"Failed to create media object. Error: {response.json()}")
    return False

# Main function to handle posting
def main():
    if len(sys.argv) != 3:
        print("Usage: python instagram.py <job_description> <media_path>")
        sys.exit(1)

    job_description = sys.argv[1]
    media_path = sys.argv[2]

    # Define S3 object key
    file_name = os.path.basename(media_path)
    object_key = f"instagram_images/{file_name}"

    # Upload media to S3
    if upload_image_to_s3(media_path, aws_bucket_name, object_key):
        image_url = get_image_url(aws_bucket_name, object_key)

        # Post to Instagram
        if post_to_instagram(image_url, job_description):
            print("Posted successfully. Deleting file from S3...")
            # Delete file from S3 after posting
            try:
                s3_client.delete_object(Bucket=aws_bucket_name, Key=object_key)
                print("File deleted from S3.")
            except Exception as e:
                print(f"Error deleting file from S3: {e}")
        else:
            print("Failed to post to Instagram.")
    else:
        print("Failed to upload media to S3.")

if __name__ == "__main__":
    main()
