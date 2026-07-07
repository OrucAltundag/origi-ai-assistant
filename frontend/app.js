async function fetchJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(body.detail || "Request failed");
  }

  return response.json();
}

async function loadNotes() {
  const notes = await fetchJson("/api/notes");
  const list = document.getElementById("notes-list");
  list.innerHTML = "";

  notes.forEach((note) => {
    const item = document.createElement("li");
    item.textContent = `${note.id}. ${note.title} - ${note.content}`;
    list.appendChild(item);
  });
}

async function loadTasks() {
  const tasks = await fetchJson("/api/tasks");
  const list = document.getElementById("tasks-list");
  list.innerHTML = "";

  tasks.forEach((task) => {
    const item = document.createElement("li");
    item.textContent = `${task.id}. ${task.title} (${task.completed ? "done" : "open"})`;
    list.appendChild(item);
  });
}

document.getElementById("note-form").addEventListener("submit", async (event) => {
  event.preventDefault();

  await fetchJson("/api/notes", {
    method: "POST",
    body: JSON.stringify({
      title: document.getElementById("note-title").value,
      content: document.getElementById("note-content").value,
    }),
  });

  event.target.reset();
  await loadNotes();
});

document.getElementById("task-form").addEventListener("submit", async (event) => {
  event.preventDefault();

  await fetchJson("/api/tasks", {
    method: "POST",
    body: JSON.stringify({
      title: document.getElementById("task-title").value,
      description: document.getElementById("task-description").value,
    }),
  });

  event.target.reset();
  await loadTasks();
});

loadNotes().catch(console.error);
loadTasks().catch(console.error);
