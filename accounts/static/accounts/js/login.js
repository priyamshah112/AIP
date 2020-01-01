$('document').ready(function () {
    var one = false, two = false;
    $("#inputPassword").keyup(function () {
        var VAL = this.value;
        var reg = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}/;

        if (reg.test(VAL)){
            $("#inputPassword").addClass("greenBorderGlow");
            $("#inputPassword").removeClass("redBorderGlow");
            one = true;
        } else {
            $("#inputPassword").removeClass("greenBorderGlow");
            $("#inputPassword").addClass("redBorderGlow");
            one = false;
        }
    });
    $("#confirmPassword").keyup(function () {
        if (this.value == $("#inputPassword").val() && one){
            $("#confirmPassword").addClass("greenBorderGlow");
            two = true;
        } else {
            $("#confirmPassword").removeClass("greenBorderGlow");
            two = false;
        }
        if (one && two){
            $("#signup").attr("disabled",false);
        } else {
            $("#signup").attr("disabled",true);
        }
    });
});
