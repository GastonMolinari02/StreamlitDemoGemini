import streamlit as st
import os
from google.cloud import storage

project_id = "{your-project}"
bucket_name = "{your-bucket}"

storage_client = storage.Client(project=project_id)

def listFiles():
    with st.spinner("Loading files..."):
        blobs = storage_client.list_blobs(bucket_name, prefix="descripcion/")
        for idx, blob in enumerate(blobs):
                if idx == 0:
                    continue
                custom_time = getattr(blob, "custom_time", None)
                if custom_time == None:
                    st.markdown("https://storage.googleapis.com/{yourproject}/" + blob.name.replace(" ", "%20"))
                else:
                    date_time = custom_time.strftime("%m/%d/%Y, %H:%M:%S")
                    st.markdown("https://storage.googleapis.com/{yourproject}/" + blob.name.replace(" ", "%20") + " " + date_time)
    st.success("Files loaded successfully!")

uploaded_video = st.file_uploader("Select a video to upload")

os.makedirs("temp", exist_ok=True)

language_options = ["ingles", "español"]
selected_language = st.selectbox("Select language", language_options)
language_code = {"ingles": "ingles", "español": "español"}[selected_language]

metadata = {
    "language": selected_language,
}

# Button to trigger upload
if st.button("Upload Video"):
    if uploaded_video is not None:

        video_path = os.path.join("temp", uploaded_video.name) 

        with open(video_path, "wb") as f:
            f.write(uploaded_video.read())

        blob = storage_client.bucket(bucket_name).blob(f"videos/{uploaded_video.name}")

        blob.metadata = metadata

        blob.upload_from_filename(video_path)

        st.write(f"Video uploaded successfully to: gs://{bucket_name}/videos/{uploaded_video.name}")

        os.remove(video_path)

st.title("History", anchor=None, help=None)

listFiles()