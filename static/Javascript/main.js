'USE STRICT'

//Account profiile update

console.log("js is here")

const searchBtn = document.getElementsByClassName('search-btn')[0]
const searchMobile = document.getElementsByClassName('search-mobile')[0]
searchBtn.addEventListener('click', ()=>{
    searchMobile.classList.toggle('hidden')
})