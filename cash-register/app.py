from flask import Flask, request, jsonify
from datetime import datetime
import random

app = Flask(__name__)

@app.route('/transactions', methods=['GET'])
def get_transactions():
    """
    Simulate a random number of transactions for a given store within a time range.
    input:  store_id, start_time, end_time
    output: JSON list of transactions with time and amount
    """
    store_id = request.args.get('store_id')
    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

     # Validate inputs
    if not store_id or not start_time or not end_time:
        return jsonify({"error": "Missing required parameters: store_id, start_time, end_time"}), 400

    try:
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
    except Exception:
        return jsonify({"error": "Invalid date format. Use ISO format, e.g., 2024-06-01T10:00:00"}), 400

    if start >= end:
        return jsonify({"error": "start_time must be before end_time"}), 400

    # Parse times
    start = datetime.fromisoformat(start_time)
    end = datetime.fromisoformat(end_time)
    # Simulate random number of transactions (up to 20)
    num_transactions = random.randint(0, 20)
    transactions = []
    for _ in range(num_transactions):
        t = start + (end - start) * random.random()
        transactions.append({
            "time": t.isoformat(),
            "amount": round(random.uniform(2, 20), 2)
        })
    return jsonify({"transactions": transactions})

if __name__ == "__main__":
    # Run the app on port 5001 (Watspeed web service runs on port 5000)
    app.run(port=5001)
