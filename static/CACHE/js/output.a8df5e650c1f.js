'USE STRICT'
console.log("js is here")
const searchBtn=document.getElementsByClassName('search-btn')[0]
const searchMobile=document.getElementsByClassName('search-mobile')[0]
searchBtn.addEventListener('click',()=>{searchMobile.classList.toggle('hidden')});let lightMode=localStorage.getItem("lightMode");const lightModeToggle=document.getElementById("light-mode-toggle");const enableLightMode=function(){document.body.classList.add('light-mode');localStorage.setItem('lightMode','enabled');};const disableLightMode=function(){document.body.classList.remove('light-mode');localStorage.setItem('lightMode','disabled');};if(lightMode==='enabled'){enableLightMode();}
lightModeToggle.addEventListener("click",()=>{lightMode=localStorage.getItem('lightMode')
if(lightMode!=='enabled'){enableLightMode()
console.log(lightMode);}
else{disableLightMode()
console.log(lightMode);}});;