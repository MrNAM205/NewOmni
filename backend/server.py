from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from scenario_engine_v2.router import run_scenario_engine

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # For now, assume the file is a text file and read its content.
        # In a real implementation, we would use a document parser to extract text
        # from different file types (PDF, images, etc.).
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Run the scenario engine on the text
            analysis_result = run_scenario_engine(text)
            
            return jsonify(analysis_result)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
