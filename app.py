import streamlit as st
import zipfile
import os
import shutil

st.set_page_config(page_title='Image Extractor',page_icon=':smile:')


# --------- Removing Streamlit's Hamburger and Footer starts ---------
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            a {text-decoration: none;}
            .css-15tx938 {font-size: 18px !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
# --------- Removing Streamlit's Hamburger and Footer ends ------------

def download_images_from_zip(zip_file_path, output_directory):
    # Create a new zip file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Get the list of files in the zip
        file_list = zip_ref.namelist()

        # Filter the files to get only the image files
        image_files = [file for file in file_list if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif','.svg'))]

        # Create a temporary directory to store the extracted images
        temp_directory = os.path.join(output_directory, 'temp')
        os.makedirs(temp_directory, exist_ok=True)

        # Extract each image file to the temporary directory
        for file in image_files:
            zip_ref.extract(file, path=temp_directory)

        # Create a new zip file to store the downloaded images
        output_zip_path = os.path.join(output_directory, 'Downloaded_images.zip')
        with zipfile.ZipFile(output_zip_path, 'w') as output_zip:
            # Add each extracted image file to the new zip
            for file in image_files:
                image_path = os.path.join(temp_directory, file)
                # Add the image file to the root of the zip
                output_zip.write(image_path, arcname=os.path.basename(file))

        # Remove the temporary directory
        shutil.rmtree(temp_directory)

        return output_zip_path


st.title("Tableau/PowerBI Image Extractor")

st.success(" Extract the images from your reports and dashboards in a single click, No more need of requesting clients for the images & logos")

# File uploader
uploaded_file = st.file_uploader("Upload the report", type=["pbix","twbx"])

if uploaded_file is not None:
    # Temporary directory to store uploaded zip file
        temp_upload_dir = './temp_upload'
        os.makedirs(temp_upload_dir, exist_ok=True)

        # Save uploaded zip file to temporary directory
        zip_file_path = os.path.join(temp_upload_dir, 'uploaded.zip')
        with open(zip_file_path, "wb") as file:
            file.write(uploaded_file.getvalue())

        # Output directory for downloaded zip file
        output_directory = './output'
        os.makedirs(output_directory, exist_ok=True)

        # Download images from zip
        output_zip_path = download_images_from_zip(zip_file_path, output_directory)

        # Download link for the zip file
        st.download_button(
            "Download Images",
            data=open(output_zip_path, "rb").read(),
            file_name="downloaded_images.zip",
            mime="application/zip"
        )

        # Cleanup temporary upload directory
        shutil.rmtree(temp_upload_dir)

st.markdown('---')
st.markdown('Made with :heart: by [Sahil Choudhary](https://www.sahilchoudhary.ml/)')

