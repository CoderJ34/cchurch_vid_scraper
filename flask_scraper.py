from flask import Flask, request

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def hello_world():
    return "Testing, someone"
@app.route("/say_name")
def say_name():
    if request.method == "GET":
        new_name = request.args.get("name")
        return f"Hey, {new_name}"
# Run the app if this file is executed
if __name__ == "__main__":
    app.run(debug=True)
