# Imports flask for web interactive
from flask import Flask
# Imports models to get the DB
from models import db
from models.user_model import User
from routes.stocks import stock_blueprint
# import cors so it can run on different ports or web
from routes.ai import ai_bp
from flask_cors import CORS


# Initialize Flask app
app = Flask(__name__)
# Tell it to allow CORS
CORS(app)


# Configuration
# Secret our API KEY DONT SHARE 
app.config['SECRET_KEY'] = 'TempKey2025'
# our database name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock_market.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)
with app.app_context():
    db.create_all()

# Register Blueprints
# Allows us to register the user
def register_blueprints(app):
    from routes.auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')    
register_blueprints(app)

app.register_blueprint(stock_blueprint, url_prefix='/stocks')
app.register_blueprint(ai_bp, url_prefix='/ai')


# Home route
@app.route('/')
def home():
    return {"message": "Welcome to the Stock Market API"}

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
