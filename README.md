HR Email Parsing and Applicant Classification System
This project automates the process of parsing job application emails, extracting essential information (such as applicant name, email, job role, resume link), and storing this data in MongoDB. It also includes a web interface built with Django to view and filter applicants based on job classifications.

Table of Contents
Project Overview
Features
Setup Instructions
Configuration
Running the Project
Usage
File Structure
License
Project Overview
The system uses IMAP to read incoming emails from a specified email account. Based on keywords in the email body, it classifies applicants into categories like "IT BASED," "Education Based," "Blue Collar," and "Others." Resumes are uploaded to Google Drive and shared through generated links. The web interface enables recruiters to filter applicants by category and view their details, including resumes.

Features
Email Parsing: Automatically fetches and processes new job application emails.
Job Role Extraction: Uses keywords to determine the job role based on the email body.
Classification: Filters applicants into different job categories.
Resume Upload: Uploads resumes to Google Drive, generating a shareable link.
Web Interface: Displays applicant data in a table with filters for easy viewing.
Setup Instructions
Prerequisites
Python 3.8 or higher
MongoDB (Local or Remote)
Google Cloud Project for Google Drive API
Django 4.1 or higher
Clone the Repository
bash
Copy code
git clone (https://github.com/Venkat-Balaji/Hr-App)
cd Hr-App
Install Dependencies
bash

pip install -r requirements.txt
Configuration
IMAP Credentials: Create a cred.yml file in the management/commands folder with your email credentials:

yaml

user: "your-email@example.com"
password: "your-password"
Google Drive API Setup:

In Google Cloud Console, create a Service Account and download the JSON key file.
Place the JSON key file in the project directory and update the SERVICE_ACCOUNT_FILE variable in listen_for_emails.py with its path.
Ensure SCOPES includes 'https://www.googleapis.com/auth/drive.file'.
MongoDB Configuration:

Ensure MongoDB is running and update the MongoDB URI in listen_for_emails.py if needed.
Running the Project
Start MongoDB (if it's not already running)
bash
# On a separate terminal or as a background service
mongod
Start the Email Listener
The email listener continuously fetches new emails and processes them.

bash
python manage.py listen_for_emails
Run Django Development Server
In another terminal, start the Django server to view the web interface.

bash
python manage.py runserver
Usage
Email Parsing: As new job application emails are received, the system extracts applicant data and stores it in MongoDB.
Applicant Classification: Access http://127.0.0.1:8000/applicants/ in your browser to view applicants.
Filtering: Use the category filter buttons to sort applicants by "IT BASED," "Education Based," "Blue Collar," and "Others."
File Structure
hr_app/management/commands/listen_for_emails.py: Fetches and processes emails.
templates/emails/applicant_list.html: Frontend for viewing applicants.
views.py: Contains view logic for filtering and displaying applicants.
License
This project is licensed under the MIT License.

This README.md covers the essential setup and usage instructions. You can further customize it by adding any additional information specific to your project setup or dependencies. Let me know if you need more customization!


**STEPS TO RUN THE PROGRAM:**

1.install the dependencies.
2. open two command prompt windows in the project directory.
3. navigate to the application (my_app) in both the windows.
4. run "_python manage.py listen_for_emails_" to actively listen to the emails
5. In another window run "_python manage.py runserver_" to locally host the application
6. open  _**http://127.0.0.1:8000/applicants/**_ in the browser
