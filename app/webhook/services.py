from datetime import datetime
from app.extensions import db

def process_event(data):
    action = data.get('action')
    timestamp = datetime.utcnow().isoformat()
    events_collection = db.db.events
    if action == 'opened' and 'pull_request' in data:
        request_id = data['pull_request'].get('id','#')
        author = data['sender'].get('login','unknown')
        action = 'pull_open'
        from_branch = data['pull_request'].get('head',{}).get('ref','unknown')
        to_branch = data['pull_request'].get('base',{}).get('ref','unknown')
        event = {
            'request_id': request_id,
            'author': author,
            'action': action,
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': timestamp
        }
        events_collection.insert_one(event)
    
    elif action == 'reopened' and 'pull_request' in data:
        request_id = data['pull_request'].get('id','#')
        author = data['sender'].get('login','unknown')
        action = 'pull_reopen'
        from_branch = data['pull_request'].get('head',{}).get('ref','unknown')
        to_branch = data['pull_request'].get('base',{}).get('ref','unknown')
        event = {
            'request_id': request_id,
            'author': author,
            'action': action,
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': timestamp
        }
        events_collection.insert_one(event)

    elif action == 'synchronize' and 'pull_request' in data:
        request_id = data['pull_request'].get('id','#')
        author = data['sender'].get('login','unknown')
        action = 'pull_synchronize'
        from_branch = data['pull_request'].get('head',{}).get('ref','unknown')
        to_branch = data['pull_request'].get('base',{}).get('ref','unknown')
        event = {
            'request_id': request_id,
            'author': author,
            'action': action,
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': timestamp
        }  
        events_collection.insert_one(event)

    elif action == 'closed' and 'pull_request' in data:
        if data['pull_request'].get('merged', False):
            request_id = data['pull_request'].get('id','#')
            author = data['sender'].get('login','unknown')
            action = 'merge'
            from_branch = data['pull_request'].get('head',{}).get('ref','unknown')
            to_branch = data['pull_request'].get('base',{}).get('ref','unknown')
            event = {
                'request_id': request_id,
                'author': author,
                'action': action,
                'from_branch': from_branch,
                'to_branch': to_branch,
                'timestamp': timestamp
            }
            events_collection.insert_one(event)
        else:    
            request_id = data['pull_request'].get('id','#')
            author = data['sender'].get('login','unknown')
            action = 'merge_cancel'
            from_branch = data['pull_request'].get('head',{}).get('ref','unknown')
            to_branch = data['pull_request'].get('base',{}).get('ref','unknown')
            event = {
                'request_id': request_id,
                'author': author,
                'action': action,
                'from_branch': from_branch,
                'to_branch': to_branch,
                'timestamp': timestamp
            }
            events_collection.insert_one(event)

    elif 'ref' in data:
        request_id = data.get('after')
        author = data['pusher'].get('name','unknown')
        action = 'push'
        from_branch = data['ref'].split('/')[-1]
        to_branch = data['repository'].get('default_branch', 'main')
        event = {
            'request_id': request_id,
            'author': author,
            'action': action,
            'from_branch': from_branch,
            'to_branch': to_branch,
            'timestamp': timestamp
        }  
        events_collection.insert_one(event)      
    
    return {"status": "success"}, 200
