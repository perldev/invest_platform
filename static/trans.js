(function(){


    // stick sigin_btn




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
    DASHBOARD.nameFormatter = function(value){
        var d = {"payin": "Инвестирование в компанию",
                 "withdraw": "Вывод средств",
                 "deal": "Покупка лота",
                 "bonus": "Возмещение сделки по лоту",
        }

        return d[value]

    };

    DASHBOARD.amountFormatter = function(value, row){
            if(row.debit_credit == "out" ){
                    return "-"+value
             }
             return value

    };


    DASHBOARD.responseHandler = function(res) {
            return {
                    "total": res["count"],
                    "rows": res["results"]
                  }
    }
    window.DASHBOARD = DASHBOARD;

    $("#trans_table").bootstrapTable();



})();
