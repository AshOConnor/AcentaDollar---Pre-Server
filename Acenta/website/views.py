from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Expense, Income, SavingsGoal
from datetime import date, datetime
from . import db
from .webforms import SearchForm
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField, IntegerField, DateField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    income = db.session.query(db.func.sum(Income.income_amount), Income.user_id).filter(Income.user_id == current_user.id).all()
    expense = db.session.query(db.func.sum(Expense.expense_amount), Expense.user_id).filter(Expense.user_id == current_user.id).all()

    income_dates = db.session.query(db.func.sum(Income.income_amount), Income.income_date, Income.user_id).filter(Income.user_id == current_user.id).group_by(Income.income_date).order_by(Income.income_date).all()
    expense_dates = db.session.query(db.func.sum(Expense.expense_amount), Expense.expense_date, Expense.user_id).filter(Expense.user_id == current_user.id).group_by(Expense.expense_date).order_by(Expense.expense_date).all()

    income_expense = []
    for total_amount, _ in income:
        income_expense.append(total_amount)

    for total_amount, _ in expense:
        income_expense.append(total_amount)

    expense_over_time = []
    expense_dates_label = []
    for exp_amount, exp_date, exp_id in expense_dates:
        expense_dates_label.append(exp_date.strftime("%m-%d-%y"))
        expense_over_time.append(exp_amount)

    income_over_time = []
    income_dates_label = []
    for inc_amount, inc_date, inc_id in income_dates:
        income_dates_label.append(inc_date.strftime("%m-%d-%y"))
        income_over_time.append(inc_amount)

    return render_template("home.html", user=current_user, income_vs_expenses = json.dumps(income_expense),
                           expense_over_time=json.dumps(expense_over_time),
                           expense_dates_label=json.dumps(expense_dates_label),
                           income_over_time=json.dumps(income_over_time),
                           income_dates_label=json.dumps(income_dates_label)
                           )

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

class ExpenseForm(FlaskForm):
    expense_name = StringField("Name", validators=[DataRequired()])
    expense_amount = IntegerField("Amount", validators=[DataRequired()])
    expense_date = DateField("Date", validators=[DataRequired()])
    submit = SubmitField("Submit")

@views.route('/edit-expense/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_expense(id):
    form = ExpenseForm()
    expense_to_update = Expense.query.get_or_404(id)

    if request.method == "POST":
        expense_to_update.expense_name = request.form['expense_name']
        expense_to_update.expense_amount = request.form['expense_amount']
        expense_to_update.expense_date = request.form['expense_date']
        try:
            db.session.commit()
            flash("Expense Updated Successfully")
            return render_template("edit_expense.html",
                                   form=form,
                                   expense_to_update=expense_to_update)
        except:
            flash("Error, try again")
            return render_template("edit_expense.html",
                                   form=form,
                                   expense_to_update=expense_to_update)
        else:
            return render_template("edit_expense.html",
                                   form=form,
                                   expense_to_update=expense_to_update)
    return render_template("edit_expense.html",
                           form=form,
                           expense_to_update=expense_to_update,
                           user=current_user)

@views.route('/income', methods=['GET', 'POST'])
def income():
    income_name = None
    income_amount = None
    income_date = None
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

@views.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    expenses = Expense.query
    income = Income.query
    if form.validate_on_submit():
        # Get data from submitted form
        expense.searched = form.searched.data
        # Query the Database
        expenses = expenses.filter(Expense.expense_name.like('%' + expense.searched + '%'))
        expenses = expenses.order_by(Expense.expense_name).all()

        # Get data from submitted form
        income.searched = form.searched.data
        # Query the Database
        income = income.filter(Income.income_name.like('%' + income.searched + '%'))
        income = income.order_by(Income.income_name).all()

        return render_template("search.html", user=current_user, form=form, searched=form.searched.data, expenses=expenses, income=income)

@views.context_processor
def base():
	form = SearchForm()
	return dict(form=form)
