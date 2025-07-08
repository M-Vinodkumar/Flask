from flask import Flask, request, render_template, jsonify
from models import insert_event, get_latest_events
from datetime import datetime

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.json
    event_type = request.headers.get('X-GitHub-Event')

    if event_type == "push":
        data = {
            "request_id": payload["after"],
            "author": payload["pusher"]["name"],
            "action": "PUSH",
            "from_branch": None,
            "to_branch": payload["ref"].split("/")[-1],
            "timestamp": datetime.utcnow().isoformat()
        }
    elif event_type == "pull_request":
        pr = payload["pull_request"]
        action = "MERGE" if pr["merged"] else "PULL_REQUEST"
        data = {
            "request_id": str(pr["id"]),
            "author": pr["user"]["login"],
            "action": action,
            "from_branch": pr["head"]["ref"],
            "to_branch": pr["base"]["ref"],
            "timestamp": pr["updated_at"]
        }
    else:
        return "Ignored", 200

    insert_event(data)
    return "Success", 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def events():
    return jsonify(get_latest_events())

if __name__ == '__main__':
    app.run(debug=True)