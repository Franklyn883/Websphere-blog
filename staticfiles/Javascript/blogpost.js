'USE STRICT'
console.log("Javascript here!!!");
const postTitle = document.getElementById('id_title');
const PostSubtitle = document.getElementById('id_subtitle');
postTitle.placeholder = 'Article Title...';
PostSubtitle.placeholder = "Article Subtile...";
const subtitle = document.getElementsByClassName('post-subtitle')[0]

const addSubtitle = document.getElementsByClassName('add-subtitle')[0]
addSubtitle.addEventListener('click',()=>{
 
 subtitle.style.display='block'

 addSubtitle.style.visibility="hidden"
})

const closeBtn = document.getElementById('close-btn')

closeBtn.addEventListener('click',()=>{
    PostSubtitle.value=""
    subtitle.style.display="none"
    addSubtitle.style.visibility="visible"
   
  
   
})