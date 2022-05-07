from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Expense, Income, SavingsGoal
from datetime import date, datetime
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
# @login_required
def home():
    income = db.session.query(db.func.sum(Income.income_amount), Income.user_id).filter(Income.user_id == current_user.id).all()
    expense = db.session.query(db.func.sum(Expense.expense_amount), Expense.user_id).filter(Expense.user_id == current_user.id).all()

    income_expense = []
    for total_amount, _ in income:
        income_expense.append(total_amount)

    for total_amount, _ in expense:
        income_expense.append(total_amount)
    return render_template("home.html", user=current_user, income_vs_expenses = json.dumps(income_expense))


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/expenses', methods=['GET', 'POST'])
def expense():
    if request.method == 'POST':
        expense_name = request.form.get('expenseName')
        expense_amount = request.form.get('expenseAmount')
        expense_date = request.form.get('expenseDate')

        expense_date = datetime.strptime(expense_date, '%Y-%m-%d')

        if len(expense_name) < 1:
            flash('Expense Name cannot be empty!', category='error')
        else:
            new_expense = Expense(expense_name=expense_name, expense_amount=expense_amount, user_id=current_user.id, expense_date=expense_date)
            db.session.add(new_expense)
            db.session.commit()
            flash('Expense added!', category='success')

    return render_template("expenses.html", user=current_user)

@views.route('/delete-expense', methods=['POST'])
def delete_expense():
    expense = json.loads(request.data)
    expenseId = expense['expenseId']
    expense = Expense.query.get(expenseId)
    expense = Expense.query.get(expenseId)
    if expense:
        if expense.user_id == current_user.id:
            db.session.delete(expense)
            db.session.commit()

    return jsonify({})

@views.route('/income', methods=['GET', 'POST'])
def income():
    if request.method == 'POST':
        income_name = request.form.get('incomeName')
        income_amount = request.form.get('incomeAmount')
        income_date = request.form.get('incomeDate')

        income_date = datetime.strptime(income_date, '%Y-%m-%d')

        if len(income_name) < 1:
            flash('Income Name cannot be empty!', category='error')
        else:
            new_income = Income(income_name=income_name, income_amount=income_amount, user_id=current_user.id, income_date=income_date)
            db.session.add(new_income)
            db.session.commit()
            flash('Income added!', category='success')

    return render_template("income.html", user=current_user)

@views.route('/delete-income', methods=['POST'])
def delete_income():
    income = json.loads(request.data)
    incomeId = income['incomeId']
    income = Income.query.get(incomeId)
    income = Income.query.get(incomeId)
    if income:
        if income.user_id == current_user.id:
            db.session.delete(income)
            db.session.commit()

    return jsonify({})

@views.route('/savingsgoals', methods=['GET', 'POST'])
def savingsgoal():
    if request.method == 'POST':
        savingsgoal_name = request.form.get('savingsgoalName')
        savingsgoal_amount = request.form.get('savingsgoalAmount')
        savingsgoal_date = request.form.get('savingsgoalDate')

        savingsgoal_date = datetime.strptime(savingsgoal_date, '%Y-%m-%d')
        if len(savingsgoal_name) < 1:
            flash('Savings Goal Name cannot be empty!', category='error')
        else:
            new_savingsgoal = SavingsGoal(savingsgoal_name=savingsgoal_name, savingsgoal_amount=savingsgoal_amount, user_id=current_user.id, savingsgoal_date=savingsgoal_date)
            db.session.add(new_savingsgoal)
            db.session.commit()
            flash('Savings Goal added!', category='success')

    return render_template("savingsgoals.html", user=current_user)

@views.route('/delete-savingsgoal', methods=['POST'])
def delete_savingsgoal():
    savingsgoal = json.loads(request.data)
    savingsgoalId = savingsgoal['savingsgoalId']
    savingsgoal = SavingsGoal.query.get(savingsgoalId)
    savingsgoal = SavingsGoal.query.get(savingsgoalId)
    if savingsgoal:
        if savingsgoal.user_id == current_user.id:
            db.session.delete(savingsgoal)
            db.session.commit()

    return jsonify({})

@views.route('/dashboard')
def dashboard():
    income = db.session.query(db.func.sum(Income.income_amount), Income.user_id).filter(Income.user_id == current_user.id).all()
    expense = db.session.query(db.func.sum(Expense.expense_amount), Expense.user_id).filter(Expense.user_id == current_user.id).all()

    income_expense = []
    for total_amount, _ in income:
        income_expense.append(total_amount)

    for total_amount, _ in expense:
        income_expense.append(total_amount)
    return render_template("dashboard.html", user=current_user, income_vs_expenses = json.dumps(income_expense))