(function(){


    // stick sigin_btn

    $("#add_funds").on("click", function(event){
            event.preventDefault();
            $("#invoice_modal").modal("show");
    });
      $("#withdraw_funds").on("click", function(event){
            event.preventDefault();
            $("#withdraw_modal").modal("show");
    });
    $("#withdraw_funds_submit").on("click", function(event){
            event.preventDefault();
           var form  = $("#withdraw_form");
           var formData = new FormData(form[0]);
           var action = form.attr("action");
            $.ajax({
                url: action,
                type: 'POST',
                data: formData,
                async: false,
                success: function (data) {
                    window.location.reload();
                },
                error: function(data){
                    $("#withdraw-error").removeClass("hidden");
                },
                cache: false,
                contentType: false,
                processData: false
            });

            return false;

    });



    var DASHBOARD = {current_table: null };

    DASHBOARD.FormatterClient = function(value, row, index) {
            return value["first_name"] + "&nbsp;" + value["last_name"]+"("+ value["loyalty"]+")";

    }
    DASHBOARD.detailFormatterFin = function(index, row) {
                var html = [];
                $.each(row, function (key, value) {

                    if(key == "currency" || key == "from_bank"|| key == "to_bank"){
                           html.push('<p><b>' + key + ':</b> ' + value["title"] + '</p>');
                    }else{
                        html.push('<p><b>' + key + ':</b> ' + value + '</p>');
                    }

                });
                return html.join('');
    }

    DASHBOARD.responseHandler = function(res) {
            return {
                    "total": res["count"],
                    "rows": res["results"]
                  }
    }
    window.DASHBOARD = DASHBOARD;

    $("#invoices_table").bootstrapTable();



})();
