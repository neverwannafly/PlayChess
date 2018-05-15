from PlayChess import app
from config import configurations

app.secret_key = configurations['_SECRET_KEY']
app.config['JSON_SORT_KEYS'] = False

app.run(debug=True)
