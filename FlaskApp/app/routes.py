# Home page route
from app import app


# url http://localhost:5000/

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"