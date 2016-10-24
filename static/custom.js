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
                    $("#greed_msg").html("<a href=\"#\">Привет, "+data.username+"</a>");

                    $("#greed_msg").removeClass("hidden");
                    $("#logout_btn").removeClass("hidden");
                    $("#dashboard").removeClass("hidden");

                    $("#login_action").modal("hide");

                },
                error: function(data){
                    $("#login_password").val("");
                    $("#errors").removeClass("hidden");

                },
                cache: false,
                contentType: false,
                processData: false
            });
            return false;


    });

    var MyCommon = {current_table: null };

    MyCommon.confirm = function(html, title, action) {
         $("#confirm_body").html(html);
         $("#confirm_title").html(title);
         $("#confirm_action").on("click", action);
         $("#confirm_modal").modal("show");
    };

    MyCommon.modal = function(html, title) {
          $("#info_body").html(html);
          $("#info_modal_label").html(title);
          $("#modal_info").modal("show");
    };

    MyCommon.hide_modal = function() {
            $("#modal_info").modal("hide");
    };

    MyCommon.hide_confirm = function() {
            $("#confirm_modal").modal("hide");
    };

    window.MyCommon = MyCommon;




})();
