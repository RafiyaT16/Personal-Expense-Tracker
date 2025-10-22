const form = document.getElementById("expense-form");
const tableBody = document.getElementById("expense-table");
const clearBtn = document.getElementById("clear-btn");

window.onload = loadExpenses;

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const category = document.getElementById("category").value.trim();
  const amount = document.getElementById("amount").value.trim();
  const date = document.getElementById("date").value;
  if (!category || !amount || !date) {
    alert("Please fill out all fields!");
    return;
  }
  try {
    const res = await fetch("http://127.0.0.1:5000/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ category, amount, date }),
    });
    if (!res.ok) {
      const err = await res.text();
      console.error("Server error:", err);
      alert("Failed to add expense!");
      return;
    }
    await loadExpenses();
    form.reset();
  } catch (error) {
    console.error("Network error:", error);
    alert("Could not connect to backend!");
  }
});

async function loadExpenses() {
  try {
    const res = await fetch(
      "http://127.0.0.1:5000/expenses?nocache=" + new Date().getTime()
    );
    const data = await res.json();
    tableBody.innerHTML = "";
    if (data.length === 0) {
      tableBody.innerHTML = `<tr><td colspan="3" style="text-align:center;">No expenses found</td></tr>`;
      return;
    }
    data.forEach((exp) => {
      const row = `
        <tr>
          <td>${exp.category}</td>
          <td>₹${exp.amount}</td>
          <td>${new Date(exp.date).toLocaleDateString()}</td>
        </tr>`;
      tableBody.innerHTML += row;
    });
  } catch (err) {
    console.error("Error loading expenses:", err);
  }
}

clearBtn.addEventListener("click", async () => {
  if (!confirm("Are you sure you want to delete all expenses?")) return;
  await fetch("http://127.0.0.1:5000/clear", { method: "DELETE" });
  await loadExpenses();
});
