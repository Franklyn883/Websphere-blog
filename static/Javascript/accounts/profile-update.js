window.addEventListener('DOMContentLoaded', (event) => {
    let textareaLocation = document.getElementById('id_location');
    let textareaBio = document.getElementById('id_bio');
    let textareaTechStack = document.getElementById('id_tech_stack');
    let displayLocation = document.getElementById('charcount__location');
    let displayBio = document.getElementById('charcount__bio');
    let displayTechStack = document.getElementById('charcount__tech-stack')

    textareaLocation.addEventListener('input',function(){
        let maxLength = this.getAttribute('maxlength');
        let currentLength = this.value.length;
    displayLocation.textContent=`${currentLength}/${maxLength}`
    })
    textareaLocation.dispatchEvent(new Event('input'))
    textareaBio.addEventListener('input',function(){
        let maxLength = this.getAttribute('maxlength');
        let currentLength = this.value.length;
    displayBio.textContent=`${currentLength}/${maxLength}`
    })
    textareaBio.dispatchEvent(new Event('input'))
    textareaTechStack.addEventListener('input',function(){
        let maxLength = this.getAttribute('maxlength');
        let currentLength = this.value.length;
    displayTechStack.textContent=`${currentLength}/${maxLength}`
    })
    textareaTechStack.dispatchEvent(new Event('input'))
})