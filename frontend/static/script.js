const  wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnpopup = document.querySelector('.btnlogin-popup');
const iconClose = document.querySelector('.icon-close');
const registerButton = document.querySelector(".register-btn");
const registrationForm = document.getElementById("registrationForm");
registerLink.addEventListener('click',()=> {
    wrapper.classList.add('active');
});
loginLink.addEventListener('click',()=> {
    wrapper.classList.remove('active');
});
btnpopup.addEventListener('click',()=> {
    wrapper.classList.add('active-popup');
});
iconClose.addEventListener('click',()=> {
    wrapper.classList.remove('active-popup');Z
});
// registrationForm.addEventListener("submit", function(event) {
    
registrationForm.addEventListener("submit", function(event) {
        console.log("Form submitted!"); // Check if this message appears in the console
        event.preventDefault();
        window.location.href = "studentdetail.html";
    });
//     event.preventDefault();})
registerButton.addEventListener("click", function() {
    console.log("Register button clicked!");
    window.location.href = "index.html";
});
