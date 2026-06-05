const API_URL = "/api";

async function addUser() {

    const name =
        document.getElementById("username").value;

    await fetch(`${API_URL}/users`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            name: name
        })

    });

    loadUsers();
}

async function loadUsers() {

    const response =
        await fetch(`${API_URL}/users`);

    const users =
        await response.json();

    const list =
        document.getElementById("users");

    list.innerHTML = "";

    users.forEach(user => {

        const li =
            document.createElement("li");

        li.innerText =
            `${user[0]} - ${user[1]}`;

        list.appendChild(li);
    });
}
