import json

CHAT_FILE = 'chats.json'

def load_chats():
    try:
        with open(CHAT_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_chats(chats):
    with open(CHAT_FILE, 'w') as f:
        json.dump(chats, f, indent=4)

def get_chat_id():
    """Generate a unique chat ID."""
    chats = load_chats()
    return str(max([int(x) for x in chats.keys()] + [0]) + 1)

def get_message_id(chat_id):
    """Generate a unique message ID within a chat."""
    chats = load_chats()
    chat = chats.get(chat_id, {})
    return str(max([int(x) for x in chat.keys()] + [0]) + 1)


from flask import Flask, request, jsonify

app2 = Flask(__name__)

@app2.route('/chats', methods=['POST'])
def create_chat():
    chat_id = get_chat_id()
    chats = load_chats()
    chats[chat_id] = {}
    save_chats(chats)
    return jsonify({'chat_id': chat_id}), 201

@app2.route('/chats/<chat_id>/messages', methods=['POST'])
def send_message(chat_id):
    chats = load_chats()
    if chat_id not in chats:
        return jsonify({'error': 'Chat not found'}), 404

    message_id = get_message_id(chat_id)
    data = request.json
    chats[chat_id][message_id] = data['message']
    save_chats(chats)

    return jsonify({'chat_id': chat_id, 'message_id': message_id, 'message': data['message']})

@app2.route('/chats/<chat_id>/messages/<message_id>', methods=['PATCH'])
def edit_message(chat_id, message_id):
    chats = load_chats()
    if chat_id not in chats or message_id not in chats[chat_id]:
        return jsonify({'error': 'Chat or message not found'}), 404

    data = request.json
    chats[chat_id][message_id] = data['content']
    save_chats(chats)

    return jsonify({'message': 'Message updated successfully', 'new_content': data['content']})

@app2.route('/chats/<chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    chats = load_chats()
    if chat_id not in chats:
        return jsonify({'error': 'Chat not found'}), 404

    del chats[chat_id]
    save_chats(chats)
    return jsonify({'message': 'Chat deleted successfully'})

if __name__ == '__main__':
    app2.run(debug=True)
