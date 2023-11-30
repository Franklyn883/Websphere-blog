'USE STRICT'
const moreOptionBtn = document.querySelector('.more-option-btn')
const moreOptionDisplay = document.querySelector('.post-option-more-content')

const displayMoreOption = ()=>{
    moreOptionDisplay.classList.toggle('hidden')
}

moreOptionBtn.addEventListener('click', displayMoreOption)


