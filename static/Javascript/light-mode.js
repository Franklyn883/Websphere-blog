//Dark-light-mode toggle
let lightMode = localStorage.getItem("lightMode");
const lightModeToggle = document.getElementById("light-mode-toggle");
const enableLightMode = function(){
    document.body.classList.add('light-mode');
    localStorage.setItem('lightMode','enabled');
};

const disableLightMode = function(){
    document.body.classList.remove('light-mode');
    localStorage.setItem('lightMode','disabled');
};

if(lightMode ==='enabled'){
    enableLightMode();
}

lightModeToggle.addEventListener("click", () => {
    lightMode = localStorage.getItem('lightMode')
  if(lightMode !=='enabled'){
    enableLightMode()
    console.log(lightMode);
  }
 else{
    disableLightMode()
    console.log(lightMode);
 }
}
);
