(function(){
    var $chart = $('#container');
    var highchart = '';
    
    var parse_lot_info = function(resp){
            var info = [];
            var data = resp.lot_info;
            info.push("<h3>" + data.name  +"</h3>");
            info.push("<p> Срок инвестиции: " + data.working_days  +"</p>");
            info.push("<p> Цена: " + data.amount  +" </p>");
            info.push("<p> Условия(%): " + data.percent  +"</p>");
            return info.join("");
    };

    // stick sigin_btn
    var buy_lot = function(id){
        $.ajax({
            url: "api/buy_lot/"+id,
            type: 'get',
            async: false,
            success: function (data) {
                var html = "Операции успешно проведена";
                MyCommon.modal(html);
                load_dashboard();
            },
            error: function(data){
                console.log("The error has been occured during buying the lot");
                var html = "The error has been occured, may be you should try later";
                MyCommon.modal(html);

            },
            cache: false,
            contentType: false,
            processData: false
        });

    };


    var buy_lot_confirm = function(){
        var id  = $(this).data("id");
        var confirm_action = function(){
                                      buy_lot(id);
                                      MyCommon.hide_confirm();
                              };
        $.ajax({
            url: "/api/lot/"+id,
            type: 'get',
            async: false,
            success: function (data) {
                 var html = parse_lot_info(data);
                 var title = "You will buy:";
                 MyCommon.confirm(html, title, confirm_action);
            },
            error: function(data){
                console.log("The error has been occured");
            },
            cache: false,
            contentType: false,
            processData: false
        });
    };

    var info_lot = function(){
        var id  = $(this).data("id");
        $.ajax({
            url: "/api/lot/"+id,
            type: 'get',
            async: false,
            success: function (data) {
                 var html = parse_lot_info(data);
                 MyCommon.modal(html);
            },
            error: function(data){
                console.log("The error has been occured");
            },
            cache: false,
            contentType: false,
            processData: false
        });



    };
    var draw_info_lot = function(data){

            var categories = data.categories;
            var result_data = data.result
            var Invest = [];
            var RefundInvest = [];
            var Wait = [];
            console.log(data);
            console.log(result_data);
            for(i in categories){
                var month = categories[i];
                if(result_data[month]){

                    Invest.push(result_data[month]["invest"]);
                    RefundInvest.push(result_data[month]["refund_investments"]);
                    Wait.push(result_data[month]["wait_income"]);


                }else{

                    Invest.push(0);
                    RefundInvest.push(0);
                    Wait.push(0);
                }

            }            

            var title = data.lot.title;
            
            highchart = Highcharts.chart(
                                "container"
                                ,{
                                chart: {
                                    type: 'column'
                                },
                                title: {
                                    text: 'Движение по  '+ title +':'
                                },
                                subtitle: {
                                    text: ''
                                },
                                xAxis: {
                                    categories:categories,
                                    crosshair: true
                                },
                                yAxis: {
                                    min: 0,
                                    title: {
                                        text: 'Инвестиции'
                                    }
                                },
                                tooltip: {
                                    headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                                    pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                                        '<td style="padding:0"><b>{point.y:.1f} USD</b></td></tr>',
                                    footerFormat: '</table>',
                                    shared: true,
                                    useHTML: true
                                },
                                plotOptions: {
                                    column: {
                                        pointPadding: 0.2,
                                        borderWidth: 0
                                    }
                                },
                                series: [ {
                                    name: 'Инвестиции',
                                    data: Invest

                                }, {
                                    name: 'Возврат инвестиций ',
                                    data: RefundInvest

                                },
                                {
                                    name: 'Ожидаемый доход',
                                    data: Wait
                                }
                                ]
                });
    };
    
    

    var info_investment = function(event){
           console.log("lot info");
           event.preventDefault();
           var lot_id = $(this).data("id");
           $.ajax({
                url: "/api/work_flow/"+lot_id,
                type: 'get',
                async: false,
                success: function (data) {
                    highchart.destroy();
                    draw_info_lot(data);
                },
                cache:false,
                contentType:false,
                processData:false
                }
            );
           
           

    };
    var draw_common = function(data){

          var categories = data.categories;
          var result_data = data.result
          var CashIn = [];
          var CashOut=[];
          var Invest = [];
          var RefundInvest = [];
          var Wait = [];

          for(i in categories){
             var month = categories[i];
             if(result_data[month]){
                CashIn.push(result_data[month]["cashin"]);
                CashOut.push(result_data[month]["cashout"]);
                Invest.push(result_data[month]["invest"]);
                RefundInvest.push(result_data[month]["refund_investments"]);
                Wait.push(result_data[month]["wait_income"]);


             }else{
                CashIn.push(0);
                CashOut.push(0);
                Invest.push(0);
                RefundInvest.push(0);
                Wait.push(0);
              }

          }
          highchart = Highcharts.chart(
                    "container"
                    ,{
                    chart: {
                        type: 'column'
                    },
                    title: {
                        text: 'Ваше денежный поток:'
                    },
                    subtitle: {
                        text: ''
                    },
                    xAxis: {
                        categories:categories,
                        crosshair: true
                    },
                    yAxis: {
                        min: 0,
                        title: {
                            text: 'Инвестиции'
                        }
                    },
                    tooltip: {
                        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                            '<td style="padding:0"><b>{point.y:.1f} USD</b></td></tr>',
                        footerFormat: '</table>',
                        shared: true,
                        useHTML: true
                    },
                    plotOptions: {
                        column: {
                            pointPadding: 0.2,
                            borderWidth: 0
                        }
                    },
                    series: [{
                        name: 'Пополнение',
                        data: CashIn

                    }, {
                        name: 'Вывод',
                        data: CashOut

                    }, {
                        name: 'Инвестиции',
                        data: Invest

                    }, {
                        name: 'Инвестиционный доход',
                        data: RefundInvest

                    },
                    {
                        name: 'Ожидаемая прибыль',
                        data: Wait

                    }
                    ]
                });



    };



    var DASHBOARD = {current_table: null };

    window.DASHBOARD = DASHBOARD;

    var load_dashboard = function(){
            $.ajax({
                url: "/api/lots",
                type: 'get',
                async: false,
                success: function (data) {
                        var $container = $("#lots2buy");
                        var lots = [];
                        var deals = data.deals2buy;
                        var total_count = 0;
                        var total_amount = 0;
                        console.log(deals)
                        for(var i in deals){
                            lots.push("<a href=\"#\" class=\"list-group-item \">"+deals[i].lot__name+"&nbsp;<span class=\"badge\">"+ deals[i].dcount
                                         + "</span><button type=\"button\" class=\"btn btn-success buy_lot\" data-id=\""+deals[i].lot_id+"\" >Купить</button>&nbsp;"+
                                           "<button type=\"button\" class=\"btn btn-info info_lot\" data-id=\""+deals[i].lot_id+"\" >Подробнее</button></a>");
                            total_count += deals[i].dcount*1;
                            total_amount += deals[i].lot__amount*deals[i].dcount;
                        }
                        lots.push('<a href="#" class="list-group-item list-group-item-success">Сумма: <span class="badge">'+ total_amount +'</span></a>');
                        lots.push('<a href="#" class="list-group-item list-group-item-success">Всего: <span class="badge">'+total_count +'</span></a>');
                        $container.html(lots.join(""));
                        $(".buy_lot").on("click", buy_lot_confirm);
                        $(".info_lot").on("click", info_lot);


                },
                error: function(data){
                    console.log("The error has been occured");
                },
                cache: false,
                contentType: false,
                processData: false
            });

            $.ajax({
                url: "/api/my_lots",
                type: 'get',
                async: false,
                success: function (data) {
                        var $container = $("#lots2sell");
                        var lots = [];
                        var deals = data.deals;
                        var total_count = 0;
                        var total_amount = 0;
                        for(var i in deals){
                            lots.push("<a href=\"#\" class=\"list-group-item info_investment\" data-id=\"" + deals[i].lot_id + "\">"+deals[i].lot__name+"&nbsp;<span class=\"badge\">"+ deals[i].dcount +
                                      "</span><button type=\"button\" class=\"btn btn-info\" data-id=\""+deals[i].lot_id+"\" >Подробнее</button></a>");
                            total_count += deals[i].dcount*1;
                            total_amount += deals[i].lot__amount*deals[i].dcount;
                        }
                        lots.push('<a href="#" class="list-group-item list-group-item-success">Сумма: <span class="badge">'+ total_amount +'</span></a>');
                        lots.push('<a href="#" class="list-group-item list-group-item-success">Всего: <span class="badge">' + total_count +'</span></a>');
                        $container.html(lots.join(""));
                        $(".info_investment").on("click", info_investment);
                },
                error: function(data){
                    console.log("The error has been occured");
                },
                cache: false,
                contentType: false,
                processData: false
            });

             $.ajax({
                url: "/api/work_flow",
                type: 'get',
                async: false,
                success: function (data) {
                    draw_common(data);
                },
                cache:false,
                contentType:false,
                processData:false
                }
                );

    };

    load_dashboard();


})();
