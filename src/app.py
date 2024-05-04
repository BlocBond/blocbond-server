from flask import Flask, json
from werkzeug.exceptions import HTTPException

#Create the Flask app instance
app = Flask(__name__)

# Import routes after app creation to avoid circular imports
# ==== Routes ====
from src.routes import index

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response
