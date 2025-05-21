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
