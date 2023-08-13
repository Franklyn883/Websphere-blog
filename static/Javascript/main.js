'USE STRICT'
console.log("javascript here!")

// to 
document.addEventListener("DOMContentLoaded", function(){
    const pathName = window.location.pathname;
    const navItems = document.querySelectorAll('.nav__link');

    navItems.forEach(item =>{
        if (item.getAttribute('href')=== pathName){
            item.classList.add('active')
        };
    });

});