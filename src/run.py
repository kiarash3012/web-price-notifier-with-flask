from src.app import app

app.run(debug=app.config['DEBUG'], theareded=True, port=80)