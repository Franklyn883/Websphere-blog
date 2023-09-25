"USE STRICT";
console.log("Javascript here!!!");
const postTitle = document.getElementById("id_title");
const PostSubtitle = document.getElementById("id_subtitle");
postTitle.placeholder = "Article Title...";
PostSubtitle.placeholder = "Article Subtile...";
const subtitle = document.getElementsByClassName("post-subtitle")[0];

const addSubtitle = document.getElementsByClassName("btn--add-subtitle")[0];
addSubtitle.addEventListener("click", () => {
    subtitle.classList.remove('hidden')

    addSubtitle.style.visibility = "hidden";
});

const closeBtn = document.getElementById("btn--close-subtitle");

closeBtn.addEventListener("click", () => {
    PostSubtitle.value = "";
    subtitle.classList.add('hidden')
    addSubtitle.style.visibility='visible   ';
});

const showCategoryBtn = document.querySelector('.btn--show-categories')
const categories = document.querySelector('.post-category__options')
const closeModal = document.querySelector('.btn--close-modal')
showCategoryBtn.addEventListener('click',()=>{
    categories.classList.remove('hidden')

})

closeModal.addEventListener('click',()=>{
categories.classList.add('hidden')
})

//function for adding image

const addCoverBtn = document.querySelector('.btn--cover')
const coverImg = document.querySelector('.post-cover')

addCoverBtn.addEventListener('click', ()=>{
    coverImg.classList.remove('hidden')
})

const tags = document.getElementById('id_tags')
tags.placeholder ='enter comma separated tags'