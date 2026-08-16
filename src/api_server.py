"""
Angry Ami API Server
Flask backend for web/desktop/mobile frontends
"""
import os
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import logging
from werkzeug.utils import secure_filename

# Load environment
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)

# Upload settings
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
MAX_FILE_SIZE = 50 * 1024 * 1024
UPLOAD_FOLDER = './data/uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize Hermes Agent in background
agent = None
agent_ready = False

def init_agent():
    """Initialize Hermes Agent in background"""
    global agent, agent_ready
    try:
        from agent import HermesAgent
        from file_processor import FileProcessor
        print("\n[INITIALIZING HERMES AGENT...]")
        agent = HermesAgent()
        agent.file_processor = FileProcessor()
        agent_ready = True
        print("[✓ HERMES AGENT READY]\n")
    except Exception as e:
        print(f"[ERROR] Agent initialization failed: {e}")
        agent_ready = False

# Suppress startup logs
logging.getLogger('werkzeug').setLevel(logging.ERROR)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'agent': 'Angry Ami', 'ready': agent_ready}), 200

@app.route('/api/greeting', methods=['GET'])
def greeting():
    """Get Ami's greeting"""
    if not agent_ready:
        return jsonify({'error': 'Agent still initializing'}), 503
    
    return jsonify({
        'greeting': agent.personality.format_greeting(),
        'status': 'ready'
    }), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with Ami"""
    if not agent_ready:
        return jsonify({'error': 'Agent still initializing'}), 503
    
    try:
        data = request.json
        user_input = data.get('message', '').strip()
        
        if not user_input:
            return jsonify({'error': 'Empty message'}), 400
        
        response = agent.chat(user_input, silent=True)
        
        return jsonify({
            'user_message': user_input,
            'ami_response': response,
            'status': 'success'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Handle document uploads for Ami to learn from"""
    if not agent_ready:
        return jsonify({'error': 'Agent still initializing'}), 503
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Use: txt, pdf, docx'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process file
        content = agent.file_processor.process_file(filepath)
        
        if not content:
            return jsonify({'error': 'Could not read file'}), 400
        
        # Save to knowledge base
        result = agent.file_processor.save_to_knowledge_base(filename, content)
        
        if result['success']:
            return jsonify({
                'status': 'success',
                'message': f'Document uploaded and learned: {filename}',
                'kb_file': result['filename'],
                'size': result['size']
            }), 200
        else:
            return jsonify({'error': result['error']}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/interests', methods=['GET'])
def get_interests():
    """Get Charlie's interests"""
    import json
    interests_path = './data/charlie_interests.json'
    
    if os.path.exists(interests_path):
        with open(interests_path, 'r') as f:
            interests = json.load(f)
        return jsonify(interests), 200
    
    return jsonify({'error': 'Interests not found'}), 404

@app.route('/api/profile', methods=['GET'])
def get_profile():
    """Get Charlie's profile"""
    import json
    profile_path = './data/charlie_profile.json'
    
    if os.path.exists(profile_path):
        with open(profile_path, 'r') as f:
            profile = json.load(f)
        return jsonify(profile), 200
    
    return jsonify({'error': 'Profile not found'}), 404

def run_server(host='0.0.0.0', port=8000, debug=False):
    """Run the API server"""
    print("=" * 80)
    print("🔥 ANGRY AMI API SERVER STARTING 🔥")
    print("=" * 80)
    print(f"Web UI: http://localhost:{port}")
    print("=" * 80)
    
    # Start agent initialization in background thread
    init_thread = threading.Thread(target=init_agent, daemon=True)
    init_thread.start()
    
    # Start Flask server
    print(f"\n * Running on http://0.0.0.0:{port}")
    print(" * Press CTRL+C to quit\n")
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    run_server()
