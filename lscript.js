const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

function logout() {
    // Perform any necessary logout actions here
    alert("You have been logged out!");
    // Redirect to the login page or homepage after logout
    window.location.href = "login.html";
}

// function handleSignIn() {
//     window.location.href = "index.html";
// }
  