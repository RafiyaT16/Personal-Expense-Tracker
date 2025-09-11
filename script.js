const form = document.getElementById("expense-form");
const tableBody = document.getElementById("expense-table");

window.onload = loadExpenses;

// Add expense
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const category = document.getElementById("category").value;
  const amount = document.getElementById("amount").value;
  const date = document.getElementById("date").value;

  const res = await fetch("http://127.0.0.1:5000/add", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ category, amount, date }),
  });

  if (res.ok) {
    form.reset();
    loadExpenses();
  }
});

// Fetch and display expenses
async function loadExpenses() {
  const res = await fetch("http://127.0.0.1:5000/expenses");
  const data = await res.json();

  tableBody.innerHTML = "";
  data.forEach((exp) => {
    const row = `<tr>
      <td>${exp.category}</td>
      <td>₹${exp.amount}</td>
      <td>${exp.date}</td>
    </tr>`;
    tableBody.innerHTML += row;
  });
}
