# Import necessary modules and classes
from flask import Blueprint, render_template

# Create the user blueprint
user = Blueprint('user', __name__)

# Define the index route for the user blueprint
@user.route('/')
def index():
    # You can render a template or return a simple message
    return render_template('index.html')



