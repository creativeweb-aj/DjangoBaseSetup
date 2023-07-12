$(document).ready(function(){
    // On loaded loader hide
    Main.Loader(false)
})

// main variable function declare
var Main = function(){ }

// Loader function to show/hide loader
Main.Loader = function(isShow){
    let element = $('#loaderId')
    if(isShow){
        element.show()
    }else{
        setTimeout(function(){
            element.hide()
        }, 1000);
    }
}