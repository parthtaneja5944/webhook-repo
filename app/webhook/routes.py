from flask import Blueprint, request, jsonify, render_template
from app.webhook.services import process_event
from datetime import datetime, timedelta
from app.extensions import db
webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    data = request.json
    print(data)
    response, status_code = process_event(data)
    return jsonify(response), status_code

@webhook.route('/get-latest-events', methods=["GET"])
def get_latest_events():
    current_time = datetime.utcnow()
    fifteen_seconds_ago = current_time - timedelta(seconds=15)
    events = list(db.db.events.find({
        'timestamp':{
            '$gte': fifteen_seconds_ago.isoformat(),
            '$lte': current_time.isoformat()
        }
    }))

    formatted_events = []
    for event in events:
        action = event.get('action')
        author = event.get('author')
        timestamp = event.get('timestamp')
        from_branch = event.get('from_branch')
        to_branch = event.get('to_branch')

        if action == 'pull_open':
            formatted_events.append(f'{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}')
        elif action == 'pull_reopen':
            formatted_events.append(f'{author} reopened the pull request from {from_branch} to {to_branch} on {timestamp}')    
        elif action == 'pull_synchronize':
            formatted_events.append(f'pull request from {from_branch} to {to_branch} on {timestamp} got synchronized')
        elif action == 'merge':
            formatted_events.append(f'{author} merged branch {from_branch} to {to_branch} on {timestamp}')  
        elif action == 'merge_cancel':
            formatted_events.append(f'Merged failed from {from_branch} to {to_branch} on {timestamp} by {author}')
        elif action == 'push':
            formatted_events.append(f'{author} pushed to {to_branch} on {timestamp}')   

    return jsonify(formatted_events),200           
                     