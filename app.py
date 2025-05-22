from app import create_app, socketio
from flask import render_template

app = create_app()

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False)