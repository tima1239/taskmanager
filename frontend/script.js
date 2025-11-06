// 💡 Для тестирования локально (FastAPI локально на 127.0.0.1:10000):
// const API_URL = "http://127.0.0.1:10000";

// ⚙️ После деплоя на Render укажи здесь URL своего сервиса:
const API_URL = "https://task-manager-cloud.onrender.com";

let token = "";

// Регистрация пользователя
async function register() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!username || !password) {
    alert("Введите логин и пароль!");
    return;
  }

  const res = await fetch(`${API_URL}/users/register?username=${username}&password=${password}`, {
    method: "POST"
  });

  if (res.ok) {
    alert("✅ Регистрация прошла успешно!");
  } else {
    const data = await res.json();
    alert("Ошибка: " + data.detail);
  }
}

// Вход пользователя
async function login() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  const res = await fetch(`${API_URL}/users/login?username=${username}&password=${password}`, {
    method: "POST"
  });

  if (!res.ok) {
    alert("❌ Неверный логин или пароль!");
    return;
  }

  const data = await res.json();
  token = data.access_token;

  document.getElementById("auth").style.display = "none";
  document.getElementById("app").style.display = "block";
  loadTasks();
}

// Загрузка задач
async function loadTasks() {
  const res = await fetch(`${API_URL}/tasks/`, {
    headers: { "Authorization": `Bearer ${token}` }
  });

  const tasks = await res.json();
  const list = document.getElementById("tasksList");
  list.innerHTML = "";

  if (tasks.length === 0) {
    list.innerHTML = "<p>Нет задач. Добавь первую!</p>";
    return;
  }

  tasks.forEach(t => {
    const li = document.createElement("li");
    li.innerHTML = `
      <span>${t.title}</span>
      <button onclick="deleteTask(${t.id})">✖</button>
    `;
    list.appendChild(li);
  });
}

// Создание задачи
async function createTask() {
  const title = document.getElementById("taskTitle").value.trim();
  if (!title) {
    alert("Введите название задачи!");
    return;
  }

  const res = await fetch(`${API_URL}/tasks/?title=${title}`, {
    method: "POST",
    headers: { "Authorization": `Bearer ${token}` }
  });

  if (res.ok) {
    document.getElementById("taskTitle").value = "";
    loadTasks();
  } else {
    alert("Ошибка при создании задачи");
  }
}

// Удаление задачи
async function deleteTask(id) {
  const res = await fetch(`${API_URL}/tasks/${id}`, {
    method: "DELETE",
    headers: { "Authorization": `Bearer ${token}` }
  });

  if (res.ok) {
    loadTasks();
  } else {
    alert("Ошибка удаления задачи");
  }
}

// Выход пользователя
function logout() {
  token = "";
  document.getElementById("auth").style.display = "block";
  document.getElementById("app").style.display = "none";
}
