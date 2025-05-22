from datetime import datetime, timedelta
import threading
import time
import requests
from flask import request
from flask_socketio import emit

# Status tracking
active_clients = set()
store_status = {1: "unknown", 2: "unknown"}

def calculate_status(transaction_count: int) -> str:
    """Determine store status based on transaction volume"""
    if transaction_count > 15:
        return "busy"
    elif transaction_count > 5:
        return "normal"
    return "quiet"

def fetch_transactions(store_id: int) -> list:
    """Fetch transactions from cash register API"""
    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=10)
    
    params = {
        "store_id": store_id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat()
    }
    
    try:
        response = requests.get("http://localhost:5001/transactions", params=params)
        return response.json().get("transactions", []) if response.status_code == 200 else []
    except requests.exceptions.RequestException:
        return []

def update_store_status(app):
    """Background thread: Periodically update store status"""
    with app.app_context():
        from flask_socketio import SocketIO
        socketio = SocketIO()
        socketio.init_app(app)
        
        print("Background status update thread started")
        while True:
            for store_id in store_status:
                transactions = fetch_transactions(store_id)
                new_status = calculate_status(len(transactions))
                print(f"Store {store_id} transaction count: {len(transactions)}, status: {new_status}")
                if new_status != store_status[store_id]:
                    store_status[store_id] = new_status
                    print(f"Store {store_id} new status: {new_status}")
                    socketio.emit('status_update', {
                        'store_id': store_id,
                        'status': new_status,
                        'timestamp': datetime.now().isoformat()
                    }, namespace='/', room=list(active_clients))
            time.sleep(10)

def register_socketio_handlers(sio, app):
    """Register all SocketIO event handlers"""
    
    # Start background thread with app instance
    thread = threading.Thread(target=update_store_status, args=(app,))
    thread.daemon = True
    thread.start()
    print(f"Status update thread state: {'Running' if thread.is_alive() else 'Not started'}")

    @sio.on('connect', namespace='/')
    def handle_connect():
        active_clients.add(request.sid)
        print(f"Client connected: {request.sid}")
        emit('connection_ack', {'message': 'Connection established'})

    @sio.on('disconnect', namespace='/')
    def handle_disconnect():
        active_clients.discard(request.sid)
        print(f"Client disconnected: {request.sid}")