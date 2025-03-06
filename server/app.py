from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import json
from werkzeug.security import generate_password_hash, check_password_hash
from models import Recipe, ScrapedItem, User  # Import all models
import sqlite3

from config import app, db

##################### TO DO ######################
# BACK BUTTON ON RECIPE DETAIL PAGE
# ADD LOGOS FOR GROCERY STORES
#STYLE BABY
#
#PRESENT
##################################################





# Set the secret key to a random value
app.secret_key = 'your_secret_key_here'

# Ensure the instance folder exists
if not os.path.exists(os.path.join(os.getcwd(), 'instance')):
    os.makedirs(os.path.join(os.getcwd(), 'instance'))

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"status": "error", "message": "Invalid input"}), 400

    user = User.query.filter_by(username=data['username']).first()
    if user:
        # Existing user, check password
        if user.check_password(data['password']):
            login_user(user)
            return jsonify({"status": "success", "message": "Logged in successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid username or password"}), 401
    else:
        # New user, create account
        if not data.get('retypePassword') or data['password'] != data['retypePassword']:
            return jsonify({"status": "error", "message": "Passwords do not match"}), 400

        user = User(username=data['username'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return jsonify({"status": "success", "message": "User created and logged in successfully"}), 201

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"status": "success", "message": "Logged out successfully"}), 200

@app.route('/')
@login_required
def index():
    return jsonify({"message": "Welcome to the Recipe API"}), 200

@app.route('/scraped_items', methods=['POST'])
def receive_scraped_items():
    scraped_items = request.json

    # Connect to the SQLite database (or create it if it doesn't exist)
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'whole_foods.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scraped_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            discount TEXT NOT NULL
        )
    ''')

    # Clear the table before inserting new items
    cursor.execute('DELETE FROM scraped_items')

    # Insert the new items into the database
    cursor.executemany('INSERT INTO scraped_items (name, discount) VALUES (?, ?)', [(item['name'], item['discount']) for item in scraped_items])

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    return jsonify({"message": "Scraped items received and stored successfully"}), 200

@app.route('/api/discounted-items', methods=['GET'])
def get_discounted_items():
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'whole_foods.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('SELECT name, discount FROM scraped_items')
    items = cursor.fetchall()

    conn.close()

    return jsonify([{"name": item[0], "discount": item[1]} for item in items])

@app.route('/scraped_items', methods=['GET'])
@login_required
def get_scraped_items():
    scraped_items = ScrapedItem.query.all()
    return jsonify([item.serialize() for item in scraped_items]), 200

@app.route('/recipes', methods=['POST'])
@login_required
def create_recipes():
    data = request.get_json()
    if data:
        try:
            # Check if data is a list
            if isinstance(data, list):
                recipes = []
                for item in data:
                    recipe = Recipe(
                        title=item['title'],
                        ingredients=item['ingredients'],
                        steps=item['steps']
                    )
                    db.session.add(recipe)
                    recipes.append(recipe)
                db.session.commit()
                return jsonify({"status": "success", "data": [recipe.serialize() for recipe in recipes]}), 201
            else:
                # Handle single recipe
                recipe = Recipe(
                    title=data['title'],
                    ingredients=data['ingredients'],
                    steps=data['steps']
                )
                db.session.add(recipe)
                db.session.commit()
                return jsonify({"status": "success", "data": recipe.serialize()}), 201
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    else:
        return jsonify({"status": "error", "message": "No data received"}), 400

@app.route('/recipes', methods=['GET'])
@login_required
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify([recipe.serialize() for recipe in recipes]), 200

@app.route('/api/recipes', methods=['GET'])
def get_all_recipes():
    recipes = Recipe.query.all()
    return jsonify([recipe.serialize() for recipe in recipes]), 200

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"status": "error", "message": "Internal server error"}), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"status": "error", "message": "Not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5555)


