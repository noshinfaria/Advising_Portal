var recommended=document.getElementById('recommended');
var fgrade=document.getElementById('fgrade');
var dd=document.getElementById('dd');
var retake=document.getElementById('retake');
document.getElementById("fgradebtn").addEventListener("click", ()=>{
    fgrade.style.display='block'
    recommended.style.display='none'
    dd.style.display='none'
    retake.style.display='none'
});

document.getElementById("recommendedbtn").addEventListener("click", ()=>{
    fgrade.style.display='none'
    recommended.style.display='block'
    dd.style.display='none'
    retake.style.display='none'
});

document.getElementById("dbtn").addEventListener("click", ()=>{
    fgrade.style.display='none'
    recommended.style.display='none'
    dd.style.display='block'
    retake.style.display='none'
});

document.getElementById("retakebtn").addEventListener("click", ()=>{
    fgrade.style.display='none'
    recommended.style.display='none'
    dd.style.display='none'
    retake.style.display='block'
});