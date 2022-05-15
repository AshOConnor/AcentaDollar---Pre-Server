
function deleteExpense(expenseId) {
  fetch("/delete-expense", {
    method: "POST",
    body: JSON.stringify({ expenseId: expenseId }),
  }).then((_res) => {
    window.location.href = "/expenses";
  });
}

function deleteIncome(incomeId) {
  fetch("/delete-income", {
    method: "POST",
    body: JSON.stringify({ incomeId: incomeId }),
  }).then((_res) => {
    window.location.href = "/income";
  });
}

function deleteSavingsGoal(savingsgoalId) {
  fetch("/delete-savingsgoal", {
    method: "POST",
    body: JSON.stringify({ savingsgoalId: savingsgoalId }),
  }).then((_res) => {
    window.location.href = "/savingsgoals";
  });
}

function editExpense(expenseId) {
  fetch("/edit-expense/<int:id>", {
    method: "POST",
    body: JSON.stringify({ expenseId: expenseId }),
  }).then((_res) => {
    window.location.href = "/expenses";
  });
}