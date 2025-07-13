from flask import Flask, request, send_file, jsonify
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>PNG To JPG Converter</h1>
    <form method="POST" action="/convert" enctype="multipart/form-data">
        <input type="file" name="image" accept=".png"><br><br>
        <input type="submit" value="Convert">
    </form>
    """

@app.route('/convert', methods=['POST'])
def convert_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image found"}), 500

    file = request.files['image']
    try:
        img = Image.open(file.stream)
        if img.format != 'PNG':
            return jsonify({"error": "PNG Files only!!"}), 500
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img_byte_stream = io.BytesIO()
        img.save(img_byte_stream, format='JPEG')
        img_byte_stream.seek(0)
        base_name = os.path.splitext(file.filename)[0]
        return send_file(
            img_byte_stream,
            mimetype='image/jpeg',
            as_attachment=True,
            download_name=f"{base_name}.jpg"
        )
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Image conversion failed"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
