const form = document.getElementById("task-form");
const titleInput = document.getElementById("title");
const formError = document.getElementById("form-error");
const list = document.getElementById("task-list");
const empty = document.getElementById("empty");

async function load() {
  const [tasksRes, statsRes] = await Promise.all([
    fetch("/api/tasks"),
    fetch("/api/stats"),
  ]);
  const tasks = await tasksRes.json();
  const stats = await statsRes.json();

  document.getElementById("stat-total").textContent = stats.total;
  document.getElementById("stat-done").textContent = stats.done;
  document.getElementById("stat-pending").textContent = stats.pending;

  list.innerHTML = "";
  empty.hidden = tasks.length > 0;

  for (const task of tasks) {
    const item = document.createElement("li");
    const title = document.createElement("span");
    title.textContent = task.title;
    if (task.done) title.className = "done";

    const actions = document.createElement("div");
    actions.className = "actions";

    if (!task.done) {
      const doneButton = document.createElement("button");
      doneButton.type = "button";
      doneButton.className = "ghost";
      doneButton.textContent = "Done";
      doneButton.addEventListener("click", () => completeTask(task.id));
      actions.appendChild(doneButton);
    }

    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.className = "danger";
    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", () => deleteTask(task.id));
    actions.appendChild(deleteButton);

    item.append(title, actions);
    list.appendChild(item);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  formError.hidden = true;
  const response = await fetch("/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title: titleInput.value }),
  });
  if (!response.ok) {
    const body = await response.json();
    formError.textContent = body.error || "Could not add task";
    formError.hidden = false;
    return;
  }
  titleInput.value = "";
  await load();
});

async function completeTask(id) {
  await fetch(`/api/tasks/${id}/complete`, { method: "POST" });
  await load();
}

async function deleteTask(id) {
  await fetch(`/api/tasks/${id}`, { method: "DELETE" });
  await load();
}

load();
