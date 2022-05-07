from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date, datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    expenses = db.relationship('Expense')
    income = db.relationship('Income')
    savingsgoals = db.relationship('SavingsGoal')

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense_name = db.Column(db.String(150))
    expense_amount = db.Column(db.String(150))
    expense_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    income_name = db.Column(db.String(150))
    income_amount = db.Column(db.String(150))
    income_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class SavingsGoal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    savingsgoal_name = db.Column(db.String(150))
    savingsgoal_amount = db.Column(db.String(150))
    savingsgoal_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))