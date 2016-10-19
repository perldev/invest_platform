(function(){


    // stick sigin_btn

    $("#sigin_btn").on("click", function(event){
            event.preventDefault();
            var formData = new FormData($("#form_login")[0]);
            $.ajax({
                url: "/auth_login",
                type: 'POST',
                data: formData,
                async: true,
                success: function (data) {
                    console.log("ok");
                    $("#regis_nav").addClass("hidden");
                    $("#login_nav").addClass("hidden");
                    $("#greed_msg").html("<a href=\"#\">Hello, "+data.username+"</a>");
                    $("#greed_msg").removeClass("hidden");
                    $("#logout_btn").removeClass("hidden");


                    $("#login_action").modal("hide");

                },
                error: function(data){
                    $("#errors").removeClass("hidden");

                },
                cache: false,
                contentType: false,
                processData: false
            });
            return false;


    });





})();
