from flask import Flask

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def hello_world():
    return "Hello, World!"

# Run the app if this file is executed
if __name__ == "__main__":
    app.run(debug=True)
