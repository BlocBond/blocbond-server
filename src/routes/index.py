from src.app import app

@app.route("/", methods=["GET"])
def index():
    return f"Welcome to BlocBond backend!"