$(document).ready(function(){
    numberEvent()
})

function numberEvent(){
    $("input[name=mobile_number]").on('keypress', function (e) {
        var keyCode = e.which ? e.which : e.keyCode
        if (!(keyCode >= 48 && keyCode <= 57)) {
            // $(".error").css("display", "inline");
            return false;
        }else{
            // $(".error").css("display", "none");
        }
    });
}

function blockSpecialChar(e){
    var k;
    document.all ? k = e.keyCode : k = e.which;
    return ((k > 64 && k < 91) || (k > 96 && k < 123) || k == 8 || k == 32 || (k >= 48 && k <= 57));
}