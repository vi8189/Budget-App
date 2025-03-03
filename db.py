from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cost_center = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False) 
    entries = db.relationship('Entry', backref='category', lazy=True)
    expenditures = db.relationship('Expenditure', backref='category', lazy=True)

    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError('Category name cannot be empty')
        return name.strip()

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    cost_center = db.Column(db.String(50), nullable=False)  # Add this line
    jan = db.Column(db.Float, default=0.0)
    feb = db.Column(db.Float, default=0.0)
    mar = db.Column(db.Float, default=0.0)
    apr = db.Column(db.Float, default=0.0)
    may = db.Column(db.Float, default=0.0)
    jun = db.Column(db.Float, default=0.0)
    jul = db.Column(db.Float, default=0.0)
    aug = db.Column(db.Float, default=0.0)
    sep = db.Column(db.Float, default=0.0)
    oct = db.Column(db.Float, default=0.0)
    nov = db.Column(db.Float, default=0.0)
    dec = db.Column(db.Float, default=0.0)

    @validates('year')
    def validate_year(self, key, year):
        if not isinstance(year, int) or year < 2000 or year > 2100:
            raise ValueError('Invalid year')
        return year

    @validates('description')
    def validate_description(self, key, description):
        if not description or not description.strip():
            raise ValueError('Description cannot be empty')
        return description.strip()

class Expenditure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    cost_center = db.Column(db.String(50), nullable=False)  # Add this line
    jan = db.Column(db.Float, default=0.0)
    jan_note = db.Column(db.String(200), default='')
    feb = db.Column(db.Float, default=0.0)
    feb_note = db.Column(db.String(200), default='')
    mar = db.Column(db.Float, default=0.0)
    mar_note = db.Column(db.String(200), default='')
    apr = db.Column(db.Float, default=0.0)
    apr_note = db.Column(db.String(200), default='')
    may = db.Column(db.Float, default=0.0)
    may_note = db.Column(db.String(200), default='')
    jun = db.Column(db.Float, default=0.0)
    jun_note = db.Column(db.String(200), default='')
    jul = db.Column(db.Float, default=0.0)
    jul_note = db.Column(db.String(200), default='')
    aug = db.Column(db.Float, default=0.0)
    aug_note = db.Column(db.String(200), default='')
    sep = db.Column(db.Float, default=0.0)
    sep_note = db.Column(db.String(200), default='')
    oct = db.Column(db.Float, default=0.0)
    oct_note = db.Column(db.String(200), default='')
    nov = db.Column(db.Float, default=0.0)
    nov_note = db.Column(db.String(200), default='')
    dec = db.Column(db.Float, default=0.0)
    dec_note = db.Column(db.String(200), default='')

    @validates('year')
    def validate_year(self, key, year):
        if not isinstance(year, int) or year < 2000 or year > 2100:
            raise ValueError('Invalid year')
        return year

    @validates('description')
    def validate_description(self, key, description):
        if not description or not description.strip():
            raise ValueError('Description cannot be empty')
        return description.strip()