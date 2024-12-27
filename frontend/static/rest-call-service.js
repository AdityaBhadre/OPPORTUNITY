function register() {
    var username = document.getElementById('username').value;
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    const data = {
        "username": username,
        "email": email,
        "password": password
    };

    fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Added headers to specify JSON type
        },
        body: JSON.stringify(data)
    }).then((res) => {
        if (res.status === 200) {
            alert("Registration successful!");
            // Redirect to index.html after success
            window.location.replace('http://localhost:5000/index.html');
        } else {
            alert("Registration failed!");
        }
    }).catch((err) => {
        console.log(err);
        alert("An error occurred during registration!");
    });

    setTimeout(login(),10000);
}



function addRegisterDetail() {
    console.log("in addRegisterDetail");
    var first_name = document.getElementById('first_name').value;
    var last_name = document.getElementById('last_name').value;
    var birthday_day = document.getElementById('birthay_day').value; // Correct ID
    var birthday_month = document.getElementById('birthday_month').value; // Correct ID
    var birthday_year = document.getElementById('birthday_year').value; // Correct ID
    var email = document.getElementById('email').value;
    var mobile_number = document.getElementById('mobile_number').value;
    var genderList = document.querySelectorAll('input[name="gender"]');
    let gender;
    genderList.forEach((g) => {
        if (g.checked) {
            gender = g.value;
        }
    });
    var address = document.getElementById('address').value;

    const data = {
        "first_name": first_name,
        "last_name": last_name,
        "birthday_day": birthday_day, // Use the corrected key
        "birthday_month": birthday_month,
        "birthday_year": birthday_year, // Use the corrected key
        "email": email,
        "mobile_number": mobile_number,
        "gender": gender,
        "address": address
    };

    fetch('http://localhost:5000/submit_form', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Ensure content type is set
        },
        body: JSON.stringify(data)
    })
    .then((res) => {
        if (!res.ok) {
            throw new Error('Network response was not ok');
        }
        return res.text(); // or res.json() if you want JSON response
    })
    .then((data) => {
        alert("Student Registration successful!");
        window.location.replace('http://localhost:5000/jobportal.html');
    })
    .catch((err) => {
        console.error(err);
        alert("An error occurred: " + err.message);
    });
}



function login() {
    var email = document.getElementById('login-email').value;
    var password = document.getElementById('login-password').value;

    const data = {
        "email": email,
        "password": password
    };

    fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Set the content type to JSON
        },
        body: JSON.stringify(data)
    })
    .then((res) => res.json())
    .then((data) => {
        console.log("data :: ", data);
        if (data['message'] === "success") {
            alert("Login successful!");
            // Redirect to the appropriate page based on student data
            if (data['studentDataFilled'] === 'true') {
                window.location.replace('http://localhost:5000/jobportal.html');
            } else {
                // Redirect to student detail page if no student data filled
                window.location.replace('http://localhost:5000/studentdetail.html');
            }
        } else {
            alert("Login failed! " + data['message']);
        }
    })
    .catch((err) => {
        console.error("Error occurred:", err);
        alert("An error occurred during login!");
    });
}
