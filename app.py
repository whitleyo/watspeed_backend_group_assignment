from app import create_app
from flask import render_template

app = create_app()

@app.route('/calculator')
def calculator():
    return render_template('calculator.html')

if __name__ == '__main__':
    app.run(debug=True)