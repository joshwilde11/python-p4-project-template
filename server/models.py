from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from config import db

class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Recipe {self.title}>"

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'ingredients': self.ingredients,
            'steps': self.steps
        }

class ScrapedItem(db.Model):
    __tablename__ = "scraped_items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    discount = db.Column(db.String(80), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=True)

    def __repr__(self):
        return f"<ScrapedItem {self.name}>"

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'discount': self.discount,
            'recipe_id': self.recipe_id
        }

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username
        }