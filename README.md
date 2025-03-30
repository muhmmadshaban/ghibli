# Ghibli Style Transfer App

## Overview

This project implements a Flask-based web application that applies Ghibli-style image transformations to user-uploaded images. The app uses TensorFlow's pre-trained style transfer model (`magenta/arbitrary-image-stylization-v1-256`) to stylize images. It is designed to run temporarily on Google Colab with free GPU/TPU support.

---

## Features

- **Image Upload**: Users can upload an image to be stylized.
- **Style Selection**: Users can select a Ghibli-style image from a predefined list fetched from a GitHub repository.
- **Style Transfer**: The uploaded image is processed using TensorFlow's style transfer model.
- **Download Results**: Users can download the stylized image.

---

## Prerequisites

To run this app, you need:

1. A Google account (for Google Colab).
2. Basic knowledge of Python and Flask.
3. Familiarity with Google Colab and its limitations.

---

## Setup Instructions

### Step 1: Clone the Repository
If you are using a GitHub repository, clone it to your local machine:
```sh
git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>
```

### Step 2: Open the Notebook in Google Colab
1. Open the `.ipynb` file containing the code in Google Colab.
2. Ensure you have selected a GPU runtime:
   - Go to `Runtime > Change runtime type`.
   - Select `GPU` as the hardware accelerator.

### Step 3: Mount Google Drive
The app stores uploaded images and results in Google Drive. To mount your Google Drive:
```python
from google.colab import drive
drive.mount('/content/drive')
```
Create a folder named `ghibli` in your Google Drive to store templates and uploads:
```
/content/drive/MyDrive/ghibli/
```

### Step 4: Install Dependencies
Run the following command to install required libraries:
```sh
!pip install flask tensorflow tensorflow-hub pillow requests > /dev/null
```

### Step 5: Generate SSH Key for localhost.run
Run the following commands to generate an SSH key pair:
```python
import os
os.system("mkdir -p ~/.ssh")
os.system("ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -q -N ''")
print("Your SSH public key is:")
!cat ~/.ssh/id_rsa.pub
```

### Step 6: Run the Flask App
Execute the Flask app in a background thread:
```python
import threading

def run_flask_app():
    app.run(host='0.0.0.0', port=3000)

thread = threading.Thread(target=run_flask_app)
thread.start()
```

### Step 7: Expose the App Using localhost.run
Expose the Flask app to the internet using localhost.run:
```sh
!ssh -o StrictHostKeyChecking=no -i ~/.ssh/id_rsa -R 80:localhost:3000 ssh.localhost.run
```
Once the tunnel is established, you will see a public URL (e.g., `https://<random-subdomain>.localhost.run`). Use this URL to access the app.

---

## Usage

### Access the App:
- Open the public URL provided by localhost.run in your browser.
- You will see a webpage with options to upload an image and select a Ghibli style.

### Upload an Image:
- Click the "Choose File" button to upload an image from your computer.
- Supported formats: JPEG, PNG, GIF, BMP.

### Select a Style:
- Choose a Ghibli-style image from the dropdown menu.

### Process the Image:
- Click the "Upload and Stylize" button to apply the selected style to your image.

### Download the Result:
- Once the processing is complete, you can view the stylized image on the webpage.
- Use the "Download" button to save the result to your computer.

---

## Notes

### Temporary Hosting:
- This app is hosted temporarily on Google Colab and exposed via localhost.run.
- The session will expire after 12 hours or if inactive for 30–60 minutes.
- Restart the notebook to restore the app.

### Persistent Storage:
- Uploaded images and results are stored in Google Drive under `/content/drive/MyDrive/ghibli/uploads`.

### Limitations:
- Google Colab is not designed for long-term hosting. For permanent hosting, consider platforms like Heroku, PythonAnywhere, or Render.

---

## Troubleshooting

### Session Timeout:
- If the app stops working, restart the Colab notebook and rerun all cells.

### SSH Tunnel Issues:
- If localhost.run fails, ensure the SSH key is correctly generated and try again.

### Unsupported Image Formats:
- Only JPEG, PNG, GIF, and BMP formats are supported. Convert other formats (e.g., WebP) before uploading.

---

## Acknowledgments

- TensorFlow Hub for providing the pre-trained style transfer model.
- localhost.run for free SSH tunneling.
- Google Colab for free GPU/TPU resources.

