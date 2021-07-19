//AJAX for the "Create Account" page


$(document).ready(function() {
    $("form[name=signup_form").on("submit", function(e) {
        var $form = $(this);
        var $error = $form.find(".error");
        var data = $form.serialize();
        $.ajax({
            url: "/user/signup",
            type: "POST",
            data: data,
            dataType: "json",
            success: function(resp) {
                $(".error").text("")
                $('#success-modal').modal("show")
            },
            error: function(resp) {
                $error.text(resp.responseJSON.error).removeClass("error-hidden");
            }
        });

        e.preventDefault();
    });
})


//AJAX for "Login" page


$(document).ready(function() {
    $("form[name=login_form").on("submit", function(e) {
        var $form = $(this);
        var $error = $form.find(".error");
        var data = $form.serialize();
        $.ajax({
            url: "/user/login",
            type: "POST",
            data: data,
            dataType: "json",
            success: function(resp) {
                window.location.replace("/dashboard/");
                // console.log(resp);
            },
            error: function(resp) {
                $error.text(resp.responseJSON.error).removeClass("error-hidden");
            }
        });

        e.preventDefault();
    });
})

$("#success_redirect_btn").on("click", function() {
    window.location.replace("/");
})