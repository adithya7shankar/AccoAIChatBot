from flask import Flask, request, jsonify
import psycopg2
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
import openai
app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
DATABASE_URL = "postgresql://postgres:postgres@localhost/chatbot_db"
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Create an SQLAlchemy object named `db` and bind it to your app
db = SQLAlchemy(app)

# OpenAI API key setup
openai.api_key = os.getenv("OPENAI_API_KEY")
#openai.api_key = 'youropenaiAPIkey'
# Define the Users model
class User(db.Model):
    __tablename__ = 'users'
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    sessions = db.relationship('Session', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
# Define the Sessions model
class Session(db.Model):
    __tablename__ = 'sessions'
    sessionid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)
    starttime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    messages = db.relationship('Message', backref='session', lazy=True)

# Define the Messages model
class Message(db.Model):
    __tablename__ = 'messages'
    messageid = db.Column(db.Integer, primary_key=True)
    sessionid = db.Column(db.Integer, db.ForeignKey('sessions.sessionid'), nullable=False)
    userid = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)
    messagetext = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    reply = db.Column(db.Text, nullable=False)
# Route to add a new user (as an example)
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(username=data['username'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'}), 201

# Route to fetch all users
@app.route('/users', methods=['GET'])
def get_users():
    users_list = User.query.all()
    users = [{
        'userid': user.userid,
        'username': user.username,
        'sessions': [{
            'sessionid': session.sessionid,
            'starttime': session.starttime.isoformat()  # Format datetime for JSON
        } for session in user.sessions]
    } for user in users_list]
    return jsonify(users)



# Route to handle chat requests
@app.route('/chat', methods=['POST'])
def chat_with_openai():
    data = request.get_json()
    user_input = data.get('message')
    userid = data.get('userid')
    wantnextsession = data.get('wantnextsession')
    user = User.query.filter_by(userid=userid).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check if there is an existing session within the last 30 minutes (or any other logic)
    last_session = Session.query.filter_by(userid=userid).order_by(Session.sessionid.desc()).first()
    if (last_session and (datetime.utcnow() - last_session.starttime <= timedelta(minutes=30))) and (not wantnextsession):
        new_session = last_session
    else:
        # Create a new session if no active session exists
        new_session = Session(userid=user.userid)
        db.session.add(new_session)
        db.session.commit()
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # specify the model
            messages=[{"role": "user", "content": user_input}]
        )
        chat_response = response['choices'][0]['message']['content']

        new_message = Message(sessionid=new_session.sessionid, userid=user.userid, messagetext=user_input, reply=chat_response)
        db.session.add(new_message)
        db.session.commit()

        return jsonify({
            "response": chat_response,
            "message_details": {
                "session_id": new_session.sessionid,
                "userid": user.userid
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    db.create_all()  # Creates the table if it doesn't already exist
    print("Database tables created.")
    app.run(debug=True, port=8080)
