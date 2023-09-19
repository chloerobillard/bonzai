// Validating user's login information:

function validate()
{
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;

    if (username = "Database Username" && password == "Database Password")
    {
        alert("Login successful.");

        window.location = "main_in.html"; // Will be added as the website development continues.

        return false;
    }
}