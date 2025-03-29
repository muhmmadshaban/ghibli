import matplotlib.pyplot as plt
import os
import tensorflow as tf
import numpy as np
import imghdr
from PIL import Image
import tensorflow_hub as hub
from flask import Flask, request, send_file, jsonify, render_template
from io import BytesIO
import requests
import json

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Debugging helper functions
def check_image_format(file_path):
    format_ = imghdr.what(file_path)
    if format_ not in ['jpeg', 'png', 'gif', 'bmp']:
        raise ValueError(f"Unsupported image format: {format_}. Supported formats are JPEG, PNG, GIF, BMP.")
    return format_

def verify_image_integrity(file_path):
    try:
        Image.open(file_path).verify()
        print("Image is valid.")
    except Exception as e:
        print(f"Image is corrupted: {e}")

def convert_webp_to_jpeg(webp_path, jpeg_path):
    # Load the WebP image
    webp_image = Image.open(webp_path)
    
    # Save the image as a JPEG
    webp_image.save(jpeg_path, 'JPEG')
    print(f"Converted WebP image to JPEG at: {jpeg_path}")

def load_image(image_path, max_dim=512):
    img = tf.io.read_file(image_path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    
    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    scale = max_dim / max(shape)
    new_shape = tf.cast(shape * scale, tf.int32)
    
    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img

# Function to dynamically fetch styles from GitHub
def get_github_styles(github_repo_url):
    # Replace with your GitHub repository URL
    github_api_url = f"{github_repo_url}/contents/styles"
    response = requests.get(github_api_url)
    if response.status_code == 200:
        contents = json.loads(response.text)
        ghibli_styles = {}
        for item in contents:
            if item['type'] == 'file':
                filename = item['name']
                raw_url = item['download_url']
                ghibli_styles[filename] = raw_url
        return ghibli_styles
    else:
        raise ValueError(f"Failed to fetch styles from GitHub. Status code: {response.status_code}")

# Predefined Ghibli-style images (High-quality URLs)
GITHUB_REPO_URL = "https://api.github.com/repos/muhmmadshaban/llm"
ghibli_styles = get_github_styles(GITHUB_REPO_URL)

@app.route('/')
def home():
    # Render the index.html template
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Get content image
    content_file = request.files['content']
    content_path = os.path.join(app.config['UPLOAD_FOLDER'], 'content_image.jpg')
    content_file.save(content_path)
    
    # Verify content image
    try:
        check_image_format(content_path)
        verify_image_integrity(content_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # Convert WebP to JPEG if necessary
    if imghdr.what(content_path) == "webp":
        converted_content_path = os.path.join(app.config['UPLOAD_FOLDER'], 'content_converted.jpg')
        convert_webp_to_jpeg(content_path, converted_content_path)
        content_path = converted_content_path
        check_image_format(content_path)

    # Get selected style
    selected_style = request.form.get('style')
    style_url = ghibli_styles[selected_style]
    response = requests.get(style_url)
    if response.status_code != 200:
        return jsonify({'error': f"Failed to download Ghibli style image. Status code: {response.status_code}"}), 400

    # Save style image
    style_path = os.path.join(app.config['UPLOAD_FOLDER'], 'ghibli_style.jpg')
    with open(style_path, 'wb') as f:
        f.write(response.content)

    # Validate style image format
    try:
        check_image_format(style_path)
        verify_image_integrity(style_path)
    except Exception as e:
        return jsonify({'error': f"Style image validation failed: {str(e)}"}), 400

    # Convert WebP to JPEG if necessary
    if imghdr.what(style_path) == "webp":
        converted_style_path = os.path.join(app.config['UPLOAD_FOLDER'], 'ghibli_style_converted.jpg')
        convert_webp_to_jpeg(style_path, converted_style_path)
        style_path = converted_style_path
        check_image_format(style_path)

    # Load images
    content_image = load_image(content_path)
    style_image = load_image(style_path)

    # Load the pre-trained style transfer model from TensorFlow Hub
    hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')

    # Apply Style Transfer
    stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]

    # Save stylized image
    stylized_path = os.path.join(app.config['UPLOAD_FOLDER'], 'stylized_image.jpg')
    plt.imsave(stylized_path, np.squeeze(stylized_image))

    # Return stylized image
    return send_file(stylized_path, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)