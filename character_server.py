"""
Character Display Server for Render.com
- Nhận text từ iOS app
- WebSocket broadcast đến browser
- Hiển thị nhân vật ảo + lip sync animation
Memory usage: ~50MB (chạy được trên Render free tier)
"""
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'jaremis-secret-2024')
socketio = SocketIO(app, cors_allowed_origins="*")

# Store current TTS state
current_state = {
    "is_speaking": False,
    "text": "",
    "character": "idle"
}

@app.route('/')
def index():
    """Character display page"""
    return render_template('character.html')

@app.route('/api/speak', methods=['POST'])
def speak():
    """
    iOS app gửi text khi TTS bắt đầu
    POST /api/speak
    {
        "text": "Chào bạn! Mình là Trơ ra mít",
        "is_speaking": true
    }
    """
    data = request.json
    text = data.get('text', '')
    is_speaking = data.get('is_speaking', False)
    
    current_state['text'] = text
    current_state['is_speaking'] = is_speaking
    current_state['character'] = 'talking' if is_speaking else 'idle'
    
    # Broadcast đến tất cả browsers đang kết nối
    socketio.emit('character_update', current_state, broadcast=True)
    
    return jsonify({
        "status": "success",
        "message": "Character updated"
    })

@app.route('/api/stop', methods=['POST'])
def stop():
    """iOS app gọi khi TTS kết thúc"""
    current_state['is_speaking'] = False
    current_state['character'] = 'idle'
    
    socketio.emit('character_update', current_state, broadcast=True)
    
    return jsonify({
        "status": "success",
        "message": "Character stopped"
    })

@app.route('/api/status', methods=['GET'])
def status():
    """Check server status"""
    return jsonify({
        "status": "running",
        "current_state": current_state
    })

@socketio.on('connect')
def handle_connect():
    """Browser kết nối"""
    print(f'Client connected')
    emit('character_update', current_state)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    # Development: socketio.run(app, debug=True, port=port)
    # Production (Render):
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
