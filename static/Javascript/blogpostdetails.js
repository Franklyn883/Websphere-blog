'USE STRICT'
console.log('Javascript here from blog')

revealDeleteBtn = document.querySelector('.btn--delete');
showConfirmation = document.querySelector('.delete-confirmation');
revealDeleteBtn.addEventListener('click',()=>{
showConfirmation.style.display = 'block'
})
