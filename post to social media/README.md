# **Social Media Job Posting Dashboard**

This project is a Streamlit-based dashboard that enables users to post job descriptions and images to multiple social media platforms (LinkedIn, Instagram, and Facebook) with ease. It is designed to simplify the management of job postings across platforms.

---

## **Features**

- **Post to Multiple Platforms:**  
  Users can post job descriptions and images to LinkedIn, Instagram, and Facebook, either individually or simultaneously.

- **Upload Media:**  
  Supports uploading image files to include with job postings.

- **Dynamic Feedback:**  
  Displays real-time feedback on the success or failure of each post to ensure clarity.

---

## **Tech Stack**

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Backend:** Python (using APIs for LinkedIn, Instagram, and Facebook)
- **Storage:** Local file system for media uploads

---

## **Installation**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/social-media-posting-dashboard.git
   cd social-media-posting-dashboard
### Install Dependencies
```bash
pip install -r requirements.txt
```
### Set Up API Credentials

Add your API keys and tokens for LinkedIn, Instagram, and Facebook in their respective .py files (linkedin.py, instagram.py, facebook.py).
Ensure proper configurations like access tokens, page IDs, and account IDs.

## Usage
### Run the Application

```bash
streamlit run app.py
```
### Navigate to the Dashboard

- Open your browser and go to http://localhost:8501.
### Post Job Descriptions

- Fill out the job description field and upload an image if needed.
- Use buttons to post to individual platforms or all platforms simultaneously.
