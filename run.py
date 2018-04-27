from PlayChess import app
from config import configurations

app.secret_key = configurations['_SECRET_KEY']

app.run(debug=True)
