import streamlit as st
import google.generativeai as genai
import os
import subprocess
import shutil  # To delete files after posting
from pathlib import Path

# Configure the API key for GenAI
api_key = "YOUR GEMINI API KEY"
genai.configure(api_key=api_key)

# Ensure the uploads folder exists
UPLOAD_FOLDER = "uploads"
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)

# Function to generate a job description from GenAI
def generate_job_description_with_genai(job_title, experience_text, skill_set, job_type, shift, workplace_type, education_level, selected_specification):
    prompt = f"""
    Hi, can you generate a job description for the following role?
    - Job Title: {job_title}
    - Experience Required: {experience_text}
    - Required Skills: {', '.join(skill_set)}
    - Job Type: {job_type}
    - Shift: {shift}
    - Workplace Type: {workplace_type}
    - Education Level: {education_level}
    - Field of Study: {selected_specification}

    Please generate a job description based on these details. just give me the description alone. your response is going to be used in a project
    """
    
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(history=[])

    response = chat_session.send_message(prompt)

    return response.text

# Streamlit UI
st.title("IT Job Recruitment Form")

# Input fields for job details (same as your original code)
job_titles = ["Software Engineer", "Data Scientist", "DevOps Engineer", "Systems Analyst", "Database Administrator", "Web Developer", "Marketing and sales"]
job_title = st.selectbox("Job Title", job_titles, key="job_title")
experience_options = ["Fresher"] + list(range(1, 16))
experience_years = st.selectbox("Years of Experience", experience_options, key="experience_years")
experience_text = "Fresher" if experience_years == "Fresher" else f"{experience_years} year(s)"
skills = ["Python", "Java", "JavaScript", "SQL", "HTML", "CSS", "C++", "C#", "Ruby", "PHP", "Cloud Computing", "Machine Learning", "Data Analysis", "DevOps", "Communication"]
skill_set = st.multiselect("Required Skill Set", skills, key="skill_set")
job_type = st.selectbox("Job Type", ["Full-time", "Part-time", "Internship"], key="job_type")
shift = st.selectbox("Shift", ["Morning Shift", "Night Shift"], key="shift")
workplace_type = st.selectbox("Workplace Type", ["On-site at Coimbatore", "Remote"], key="workplace_type")
education_level = st.selectbox("Education Level", ["Select", "Bachelor's Degree", "Master's Degree", "PhD", "Other", "Diploma"], key="education_level")

selected_specification = ""
if education_level != "Select":
    specifications = ["Computer Science Engineering (CSE)", "Information Technology (IT)", "Software Engineering", "Data Science", "EEE and Mech"]
    selected_specification = st.selectbox("Select Field of Study", specifications, key="specification")

# Generate job description using GenAI
if st.button("Generate Job Description"):
    job_description = generate_job_description_with_genai(job_title, experience_text, skill_set, job_type, shift, workplace_type, education_level, selected_specification)
    st.session_state['job_description'] = job_description
    st.write("Job Description generated successfully.")
    st.text_area("Generated Job Description", job_description, height=300, key="generated_job_description")

# Edit and Update the job description
if 'job_description' in st.session_state:
    edited_job_description = st.text_area("Edit Job Description", st.session_state['job_description'], height=300, key="edited_job_description")
    if st.button("Update Job Description"):
        st.session_state['job_description'] = edited_job_description
        st.write("Job Description updated successfully.")
        st.text_area("Updated Job Description", st.session_state['job_description'], height=300, key="updated_job_description")

# Displaying the final description
if 'job_description' in st.session_state:
    st.write("Final Job Description:")
    st.write(st.session_state['job_description'])

# Media upload feature
uploaded_media = st.file_uploader("Upload Media (Image/Video)", type=["jpg", "jpeg", "png", "mp4", "avi"], key="uploaded_media")
if uploaded_media is not None:
    file_path = os.path.join(UPLOAD_FOLDER, uploaded_media.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_media.getbuffer())
    st.image(file_path, caption="Uploaded Media", use_column_width=True)

def post_to_platform(script_name, media_path):
    if 'job_description' not in st.session_state:
        st.error("Please generate a job description first!")
    else:
        job_description = st.session_state['job_description']
        try:
            result = subprocess.run(["python", script_name, job_description, media_path], capture_output=True, text=True)
            if result.returncode == 0:
                st.write(f"Posted to {script_name.split('.')[0].capitalize()} successfully!")
                # os.remove(media_path)  # Delete the file after posting
                # st.write("Media file deleted after posting.")
            else:
                st.error(f"Failed to post to {script_name.split('.')[0].capitalize()}: {result.stderr}")
        except Exception as e:
            st.error(f"Error running {script_name}: {e}")


#bg image



# Buttons for posting to each platform individually and all at once
# Creating a row for individual platform buttons
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("Post to LinkedIn") and uploaded_media is not None:
        post_to_platform("linkedin.py", file_path)

with col2:
    if st.button("Post to Instagram") and uploaded_media is not None:
        post_to_platform("instagram.py", file_path)

with col3:
    if st.button("Post to Facebook") and uploaded_media is not None:
        post_to_platform("facebook.py", file_path)

# Creating a separate row for the "Post to All" button
st.markdown("---")  # Optional: Horizontal line for separation
if st.button("Post in All Media") and uploaded_media is not None:
    try:
        st.write("Posting to LinkedIn...")
        post_to_platform("linkedin.py", file_path)

        st.write("Posting to Instagram...")
        post_to_platform("instagram.py", file_path)

        st.write("Posting to Facebook...")
        post_to_platform("facebook.py", file_path)

        # Delete media file only after all attempts
        os.remove(file_path)
        st.write("Media file deleted after posting to all platforms.")
        st.success("Posted to all platforms successfully!")

    except Exception as e:
        st.error(f"An error occurred during posting: {e}")
