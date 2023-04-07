function check()
{
    var username = document.getElementById("username").value;
    var email = document.getElementById("email").value;
    var password_1 = document.getElementById("password_1").value;
    var password_2 = document.getElementById("password_2").value;

    console.log(username, email, password_1, password_2);

    fetch('auth/register', 
    {
        method: 'POST',
        headers: 
        {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify
        ({
            username: username,
            email: email,
            password_1: password_1
        })
    })
}

console.log('Working properly');
