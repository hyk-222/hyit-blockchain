// 交易所总交易量
var exchange_volumeUsd = [];   //全局变量
var exchange_name_list = ['binance', "hitbtc", "crypto", "gdax", "digifinex", "kucoin", "bkex"];

(function () {
    // var myChart = echarts.init(document.getElementById('echarts1'));
    var myChart = echarts.init(document.querySelector(".bar .chart"));
    // var exchange_name_list = ['binance', "hitbtc", "crypto", "gdax", "digifinex", "kucoin", "bkex"];
    // var exchange_volumeUsd = [];
    var exchange_percentTotalVolume = [];

    $.ajax({
        url: 'https://api.coincap.io/v2/exchanges/',
        type: 'get',
        dataType: 'json',
        async: false,
        success: function (data) {
            exchange_count_data = data;
        }
    })
    console.log(exchange_count_data)
    for (var i in exchange_name_list) {
        for (var j in exchange_count_data.data) {
            if (exchange_name_list[i] === exchange_count_data.data[j].exchangeId) {
                exchange_volumeUsd[i] = parseFloat(exchange_count_data.data[j].volumeUsd);
                exchange_percentTotalVolume[i] = parseFloat(exchange_count_data.data[j].percentTotalVolume);
            }
        }
    }
    // var exchange_percentTotalVolume = []
     var y_max=exchange_volumeUsd[0]+40000000
    console.log(y_max)
    for (var i = 0; i < exchange_volumeUsd.length; i++) {
        exchange_volumeUsd[i] = exchange_volumeUsd[i].toFixed(2)
        exchange_percentTotalVolume[i] = exchange_percentTotalVolume[i].toFixed(2)
    }
     var y_max=exchange_volumeUsd[0]+40000000
    // console.log(exchange_volumeUsd)
    option = {

        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                crossStyle: {
                    show:false,
                    color: '#e4d9d9',
                },
            },
            textStyle: {
                fontWeight: 'normal',
                fontSize: 11,
            },
        },
        grid: {
            left: '25%',
            right: '14%',
            top: '20%',
            bottom: '25%',
        },
        legend: {
            data: ['交易所交易额', '占比'],
            show:false,
            top: '8%',
            itemWidth: 13,
            itemHeight: 9,
            textStyle: {
                fontSize: 9,
            },
        },
        xAxis: [
            {
                type: 'category',
                // data: ['okex', 'bithumb', 'quoine', 'Kraken', 'lbank', 'bitflyer', 'bittrex'],
                data: exchange_name_list,
                axisPointer: {
                    type: 'shadow',
                },
                axisLabel: {
                    rotate: 30,
                    fontSize: 13,
                    color: '#e4d9d9',
                },
            },
        ],
        yAxis: [
            {
                type: 'value',
                name: '总交易量(USD)',
                position: 'left',
                nameLocation: 'end',
                nameRotate: '0',
                nameGap: 30,
                //nameLocation: 'middle',
                nameTextStyle: {
                    color: '#d8e06e',
                    fontSize: 9,
                },
                nameGap: 25,
                min: 0,
                // max: 1000000000,
                max: y_max,   //与间隔成四倍关系，如要修改倍数关系需同百分比一起修改
                interval:y_max/4,
                axisLabel: {
                    formatter: '{value}',
                    color: '#e4d9d9',
                    fontSize: 10,
                    margin: 5,
                },
            },
            // {
            //     type: 'value',
            //     show:false,
            //     name: '交易占比(%)',
            //     position: 'right',
            //     nameLocation: 'end',
            //     nameRotate: '0',
            //     nameGap: 30,
            //     //nameLocation: 'middle',
            //     nameTextStyle: {
            //         color: '#F5BA69',
            //         fontSize: 10,
            //     },
            //     nameGap: 25,
            //     min: 0,
            //     max: 40,
            //     interval: 10,
            //     axisLabel: {
            //         formatter: '{value}',
            //         color: '#F5BA69',
            //         fontSize: 9,
            //         margin: 5,
            //     },
            // },
        ],
        series: [
            {
                name: '总交易量(USD)',
                type: 'bar',
                color: '#5C92F7',
                barWidth: '50%',
                // data: [300000000, 350000000, 550000000, 280000000, 720000000, 580000000, 40000000],
                data: exchange_volumeUsd,
            },
            // {
            //     name: '交易占比(%)',
            //     show:false,
            //     type: 'scatter',
            //     yAxisIndex: 1,
            //     color: '#F5BA69',
            //     // data: [21, 15, 0.8, 7, 0.5, 0.6, 16],
            //     data: exchange_percentTotalVolume,
            // },
        ],
    };

    myChart.setOption(option);
    window.addEventListener("resize", function () {
        myChart.resize();
    });


})();

// btb今日交易额
(function () {
    // var myChart2 = echarts.init(document.getElementById('echarts3'));
    var myChart2 = echarts.init(document.querySelector(".line .chart"));
        $.ajax({
            url:'http://127.0.0.1:8000/bit_trade',
            type:'get',
            dataType:'json',
            async:false,
            success:function(data){
                bit_trade = data
            }
        })

        bit_trade_time_list = bit_trade.data.bit_trade_time_list;
        bit_trade_time_count_list = bit_trade.data.bit_trade_time_count_list;
        console.log(bit_trade_time_list)
        console.log(bit_trade_time_count_list)


        option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    lineStyle: {
                        color: '#dddc6b'
                    }
                }
            },
            // grid: {
            //     left: '0',
            //     top: '30',
            //     right: '-20',
            //     bottom: '-10',
            //     containLabel: true
            // },

            xAxis: [{
                type: 'category',
                boundaryGap: false,
                axisLabel: {
                    textStyle: {
                        color: "rgba(255,255,255,.6)",
                        fontSize: 14,
                    },
                },
                axisLine: {
                    lineStyle: {
                        color: 'rgba(255,255,255,.1)'
                    },

                },

                // data: ['3-01', '3-02', '3-03', '3-04', '3-05', '3-06', '3-07', '3-08', '3-09', '3-10', '3-11', '3-12', '3-13', '3-14', '3-15']
                data :bit_trade_time_list
            }, {

                axisPointer: {show: false},
                axisLine: {show: false},
                position: 'bottom',
                offset: 200,


            }],

            yAxis: [{
                type: 'value',
                axisTick: {show: false},
                axisLine: {
                    lineStyle: {

                        color: 'rgba(255,255,255,.1)'
                    }
                },
                axisLabel: {
                    textStyle: {

                        color: "rgba(255,255,255,.6)",
                        fontSize: 14,
                    },
                },

                splitLine: {
                    lineStyle: {

                        color: 'rgba(255,255,255,.1)',

                    }
                }
            }],
            series: [
            //     {
            //     name: '交易占比(%)',
            //         type:
            //     color: '#F5BA69',
            // },
                {
                    name: '今日总交易额',
                    type: 'line',
                    smooth: true,

                    symbol: 'circle',
                    symbolSize: 10,
                    showSymbol: true,
                    lineStyle: {

                        normal: {

                            color: 'rgba(228, 228, 126, 1)',
                            width: 2
                        }
                    },
                    areaStyle: {
                        normal: {

                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                offset: 0,
                                color: 'rgba(228, 228, 126, .8)'
                            }, {
                                offset: 0.8,
                                color: 'rgba(228, 228, 126, 0.1)'
                            }], false),
                            shadowColor: 'rgba(0, 0, 0, 0.1)',
                        }
                    },
                    itemStyle: {
                        normal: {
                            color: '#dddc6b',
                            borderColor: 'rgba(221, 220, 107, .1)',
                            borderWidth: 12
                        }
                    },
                    // data: [600, 200, 600, 200, 400, 200, 400, 300, 400, 300, 400, 300, 200, 400, 200],
                    data :bit_trade_time_count_list
                }
            ]
        };


        // 使用刚指定的配置项和数据显示图表。
        myChart2.setOption(option);
        window.addEventListener("resize", function () {
            myChart2.resize();
        });


    // // 基于准备好的dom，初始化echarts实例
    // var myChart = echarts.init(document.querySelector(".line .chart"));
    //
    // // (1)准备数据
    // var data = {
    //     year: [
    //         [24, 40, 101, 134, 90, 230, 210, 230, 120, 230, 210, 120],
    //         [40, 64, 191, 324, 290, 330, 310, 213, 180, 200, 180, 79]
    //     ]
    // };
    //
    // // 2. 指定配置和数据
    // var option = {
    //     color: ["#00f2f1", "#ed3f35"],
    //     tooltip: {
    //         // 通过坐标轴来触发
    //         trigger: "axis"
    //     },
    //     legend: {
    //         // 距离容器10%
    //         right: "10%",
    //         // 修饰图例文字的颜色
    //         textStyle: {
    //             color: "#4c9bfd"
    //         }
    //         // 如果series 里面设置了name，此时图例组件的data可以省略
    //         // data: ["邮件营销", "联盟广告"]
    //     },
    //     grid: {
    //         top: "20%",
    //         left: "3%",
    //         right: "4%",
    //         bottom: "3%",
    //         show: true,
    //         borderColor: "#012f4a",
    //         containLabel: true
    //     },
    //
    //     xAxis: {
    //         type: "category",
    //         boundaryGap: false,
    //         data: [
    //             "1月",
    //             "2月",
    //             "3月",
    //             "4月",
    //             "5月",
    //             "6月",
    //             "7月",
    //             "8月",
    //             "9月",
    //             "10月",
    //             "11月",
    //             "12月"
    //         ],
    //         // 去除刻度
    //         axisTick: {
    //             show: false
    //         },
    //         // 修饰刻度标签的颜色
    //         axisLabel: {
    //             color: "rgba(255,255,255,.7)"
    //         },
    //         // 去除x坐标轴的颜色
    //         axisLine: {
    //             show: false
    //         }
    //     },
    //     yAxis: {
    //         type: "value",
    //         // 去除刻度
    //         axisTick: {
    //             show: false
    //         },
    //         // 修饰刻度标签的颜色
    //         axisLabel: {
    //             color: "rgba(255,255,255,.7)"
    //         },
    //         // 修改y轴分割线的颜色
    //         splitLine: {
    //             lineStyle: {
    //                 color: "#012f4a"
    //             }
    //         }
    //     },
    //     series: [
    //         {
    //             name: "新增项目",
    //             type: "line",
    //             stack: "总量",
    //             // 是否让线条圆滑显示
    //             smooth: true,
    //             data: data.year[0]
    //         },
    //         {
    //             name: "新增技能",
    //             type: "line",
    //             stack: "总量",
    //             smooth: true,
    //             data: data.year[1]
    //         }
    //     ]
    // };
    // // 3. 把配置和数据给实例对象
    // myChart.setOption(option);
    //
    // // 重新把配置好的新数据给实例对象
    // myChart.setOption(option);
    // window.addEventListener("resize", function () {
    //     myChart.resize();
    // });

})();

// BTC今日交易详情
(function () {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.querySelector(".pie .chart"));
    $.ajax({
            url:"http://127.0.0.1:8000/today_trade",
            type:"get",
            dataType:"json",
            async:false,
            success:function (data){
                count_data = data
            }
        })
        today_active = count_data.data[0].today_active
        today_count = count_data.data[0].today_count
        trade_btc = count_data.data[0].trade_btc
        transaction_count = count_data.data[0].transaction_count
    option = {

            //backgroundColor:'#040f23',
            tooltip: {},
            animationDurationUpdate: function (idx) {
                // 越往后的数据延迟越大
                return idx * 100;
            },
            animationEasingUpdate: 'bounceIn',
            color: ['#fff', '#fff', '#fff'],
            series: [{
                type: 'graph',
                layout: 'force',
                force: {
                    repulsion: 30,
                    edgeLength: 15
                },
                roam: true,
                label: {
                    normal: {
                        show: true,
                        position: 'inside',
                        formatter: '{c}' + '\n\n' + '{b}',
                        fontSize: 11,
                        fontStyle: '400',
                    }
                },
                data: [{
                    "name": "今日交易额",
                    "value": today_count,
                    x: 80,
                    y: 6,
                    "symbolSize": 100,
                    "draggable": true,
                    "itemStyle": {
                        "normal": {
                            "borderColor": "#ff8400",
                            "borderWidth": 1,
                            "shadowBlur": 30,
                            "shadowColor": "#ff8400",
                            "color": "#11213b"
                        }
                    }
                }, {
                    "name": "今日交易笔数",
                    "value": transaction_count,
                    x: 0,
                    y: 0,
                    "symbolSize": 100,
                    "draggable": true,
                    "itemStyle": {
                        "normal": {
                            "borderColor": "#03fc62",
                            "borderWidth": 1,
                            "shadowBlur": 20,
                            "shadowColor": "#03fc62",
                            "color": "#11213b"
                        }
                    },

                }, {
                    "name": "今日活跃地址数",
                    "value": today_active,
                    x: 0,
                    y: 0,
                    "symbolSize": 100,
                    "draggable": true,
                    "itemStyle": {
                        "normal": {
                            "borderColor": "#aa61b2",
                            "borderWidth": 1,
                            "shadowBlur": 20,
                            "shadowColor": "#aa61b2",
                            "color": "#11213b"
                        }
                    }
                }, {
                    "name": "BTC",
                    "value": trade_btc,
                    "symbolSize": 120,
                    x: 0,
                    y: 0,
                    "draggable": true,
                    "itemStyle": {
                        "normal": {
                            "borderColor": "#0a95e6",
                            "borderWidth": 2,
                            "shadowBlur": 20,
                            "shadowColor": "#0a95e6",
                            "color": "#11213b"
                        }
                    }
                    // },
                    //{
                    //     "name": "四级",
                    //     "value": "NO.5",
                    //     x: 0,
                    //     y: 0,
                    //     "symbolSize":120,
                    //     "draggable": true,
                    //     "itemStyle": {
                    //         "normal": {
                    //             "borderColor": "#00fff7",
                    //             "borderWidth": 4,
                    //             "shadowBlur": 20,
                    //             "shadowColor": "#00fff7",
                    //             "color": "#11213b"
                    //         }
                    //     }
                    // }, {
                    //     "name": "五级",
                    //     "value": "NO.6",
                    //     x: 0,
                    //     y: 0,
                    //     "symbolSize": 120,
                    //     "draggable": true,
                    //     "itemStyle": {
                    //         "normal": {
                    //             "borderColor": "#f06467",
                    //             "borderWidth": 4,
                    //             "shadowBlur": 20,
                    //             "shadowColor": "#f06467",
                    //             "color": "#11213b"
                    //         }
                    //     }
                    // }, {
                    //     "name": "六级",
                    //     "value": "NO.7",
                    //     x: 0,
                    //     y: 0,
                    //     "symbolSize":120,
                    //     "draggable": true,
                    //     "itemStyle": {
                    //         "normal": {
                    //             "borderColor": "#f06467",
                    //             "borderWidth": 4,
                    //             "shadowBlur": 20,
                    //             "shadowColor": "#f06467",
                    //             "color": "#11213b"
                    //         }
                    //     }
                    // }, {
                    //     "name": "七级",
                    //     "value": "NO.8",
                    //     x: 0,
                    //     y: 0,
                    //     "symbolSize": 120,
                    //     "draggable": true,
                    //     "itemStyle": {
                    //         "normal": {
                    //             "borderColor": "#03fc62",
                    //             "borderWidth": 4,
                    //             "shadowBlur": 20,
                    //             "shadowColor": "#03fc62",
                    //             "color": "#11213b"
                    //         }
                    //     }
                    // }, {
                    //     "name": "八级",
                    //     "value": "NO.9",
                    //     x: 0,
                    //     y: 0,
                    //     "symbolSize": 120,
                    //     "draggable": true,
                    //     "itemStyle": {
                    //         "normal": {
                    //             "borderColor": "#00fff7",
                    //             "borderWidth": 4,
                    //             "shadowBlur": 20,
                    //             "shadowColor": "#00fff7",
                    //             "color": "#11213b"
                    //         }
                    //     }
                    // }, {
                    //     "name": "九级",
                    //     "value": "NO.10",
                    //     x: 0,
                    //     y: 0,
                    //     "symbolSize":120,
                    //     "draggable": true,
                    //     "itemStyle": {
                    //         "normal": {
                    //             "borderColor": "#f06467",
                    //             "borderWidth": 4,
                    //             "shadowBlur": 20,
                    //             "shadowColor": "#f06467",
                    //             "color": "#11213b"
                    //         }
                    //     }
                }],
                links: [{
                    "source": "今日交易额",
                    "target": "BTC"
                },
                    {
                        "source": "今日交易笔数",
                        "target": "BTC"
                    },
                    {
                        "source": "今日活跃地址数",
                        "target": "BTC"
                    },
                    // {
                    //     "source": "四级",
                    //     "target": "总集"
                    // },
                    // {
                    //     "source": "五级",
                    //     "target": "总集"
                    // },
                    // {
                    //     "source": "六级",
                    //     "target": "总集"
                    // }, {
                    //     "source": "七级",
                    //     "target": "总集"
                    // }, {
                    //     "source": "八级",
                    //     "target": "总集"
                    // }, {
                    //     "source": "九级",
                    //     "target": "总集"
                    // }
                ]
            }]
        };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    window.addEventListener("resize", function () {
        myChart.resize();
    });
})();


// 今日交易大额地址排行

(function () {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.querySelector(".bar1 .chart"));

     $.ajax({
            url:"http://127.0.0.1:8000/rank_value",
            type:'get',
            dataType:'json',
            async:false,
            success:function (data){
                rank_data = data
            }
        })
       address_1=rank_data.data[0].rank_recipient
        address_2=rank_data.data[1].rank_recipient
    address_3=rank_data.data[2].rank_recipient
        address_4=rank_data.data[3].rank_recipient
            address_5=rank_data.data[4].rank_recipient
         console.log(address_1)
        value_1=rank_data.data[0].rank_value
        value_2=rank_data.data[1].rank_value
         value_3=rank_data.data[2].rank_value
        value_4=rank_data.data[3].rank_value
        value_5=rank_data.data[4].rank_value
        // var i
        // function recipient_data(i,recipient){
        //     var recipient_handle=document.getElementById(recipient)
        //     recipient_handle.innerHTML=rank_data.data[i].rank_recipient
        // }
        // function value_data(i,value){
        //     var value_handle = document.getElementById(value)
        //     value_handle.innerHTML=rank_data.data[i].rank_value
        // }
        // recipient_list=['recipient_1','recipient_2','recipient_3','recipient_4','recipient_5']
        // for(i=0;i<recipient_list.length;i++){
        //     recipient_data(i,recipient_list[i])
        // }
        // value_list = ['value_1','value_2','value_3','value_4','value_5']
        // for(i=0;i<value_list.length;i++){
        //     value_data(i,value_list[i])
        // }


        console.log(rank_data)
   // var data = [90, 80, 75, 65, 65];
    var titlename = [address_1, address_2, address_3, address_4, address_5];
    var valdata = [value_1, value_2, value_3, value_4, value_5];
    var myColor = ["#1089E7", "#F57474", "#56D0E3", "#F8B448", "#8B78F6"];
    option = {
        //图标位置
        grid: {
            top: "10%",
            left: "70%",
            right:"20%",
            bottom: "10%"
        },
        xAxis: {
            show: false
        },
        yAxis: [
            {
                show: true,
                data: titlename,
                inverse: true,
                axisLine: {
                    show: false
                },
                splitLine: {
                    show: false
                },
                axisTick: {
                    show: false
                },
                axisLabel: {
                    color: "#fff",

                    rich: {
                        lg: {
                            backgroundColor: "#339911",
                            color: "#fff",
                            borderRadius: 5,
                            padding: 60,
                            align: "center",
                            width: 5,
                            height: 15,

                        }
                    }
                }
            },
            {
                show: true,
                inverse: true,
                data: valdata,
                axisLabel: {
                    textStyle: {
                        fontSize: 12,
                        color: "#fff"
                    }
                }
            }
        ],
        // series: [
        //     {
        //         name: "条",
        //         type: "bar",
        //         yAxisIndex: 0,
        //         data: data,
        //         barCategoryGap: 50,
        //         barWidth: 15,
        //         itemStyle: {
        //             normal: {
        //                 barBorderRadius: 20,
        //                 color: function (params) {
        //                     var num = myColor.length;
        //                     return myColor[params.dataIndex % num];
        //                 }
        //             }
        //         },
        //         label: {
        //             normal: {
        //                 show: true,
        //                 position: "inside",
        //                 formatter: "{c}%"
        //             }
        //         }
        //     },
        //     {
        //         name: "框",
        //         type: "bar",
        //         yAxisIndex: 1,
        //         barCategoryGap: 50,
        //         data: [100, 100, 100, 100, 100],
        //         barWidth: 15,
        //         itemStyle: {
        //             normal: {
        //                 color: "none",
        //                 borderColor: "#00c1de",
        //                 borderWidth: 3,
        //                 barBorderRadius: 15
        //             }
        //         }
        //     }
        // ]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
    window.addEventListener("resize", function () {
        myChart.resize();
    });
})();
// 24小时价格监控
(function () {
    // var myChart2 = echarts.init(document.getElementById('echarts2'));
    var myChart2 = echarts.init(document.querySelector(".line1 .chart"));
    var timestamp = Date.parse(new Date());
    var our_timestamp = timestamp + 1000 * 60 * 60 * 8
    var before = timestamp - 1000 * 60 * 60 * 24
    var bitcoin_price = []
    var ethereum_price = []
    var tether_price = []
    var timelist = []

    var fun1 = $.ajax({
            url: "https://api.coincap.io/v2/assets/bitcoin/history", type: 'GET', data: {
                'interval': 'h1',
                'start': before,
                'end': timestamp
            }, dataType: 'json'
        }),
        fun2 = $.ajax({
            url: "https://api.coincap.io/v2/assets/ethereum/history", type: 'GET', data: {
                'interval': 'h1',
                'start': before,
                'end': timestamp
            }, dataType: 'json'
        }),
        fun3 = $.ajax({
            url: "https://api.coincap.io/v2/assets/maker/history", type: 'GET', data: {
                'interval': 'h1',
                'start': before,
                'end': timestamp
            }, dataType: 'json'
        })
    $.when(fun1, fun2, fun3).then(function (data1, data2, data3) {
        console.log(data1[0]['data'])
        var regex = /([\d-]{10})T([\d:]{5})/;
        for (var i = 0; i < data1[0]['data'].length; i++) {
            bitcoin_price.push(data1[0]['data'][i]['priceUsd']);
            match = regex.exec(data1[0]['data'][i]['date']);
            timelist.push(match[2])
            console.log(timelist)
        }
        for (var i = 0; i < data2[0]['data'].length; i++) {
            ethereum_price.push(data2[0]['data'][i]['priceUsd'])
        }
        for (var i = 0; i < data3[0]['data'].length; i++) {
            tether_price.push(data3[0]['data'][i]['priceUsd'])
        }
        option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    lineStyle: {
                        color: '#dddc6b'
                    }
                }
            },
            grid: {
                left: '0',
                top: '30',
                right: '20',
                bottom: '0',
                containLabel: true
            }, legend: {
                data: ['BTC', 'ETH', 'MKR'],
                selected:{'BTC':false, 'ETH':false, 'MKR':true},
                right: 'center',
                top: 0,
                textStyle: {
                    color: "#fff"
                },
                itemWidth: 10,
                itemHeight: 8,
                // itemGap: 35
            },

            xAxis: [{
                type: 'category',
                boundaryGap: false,

                axisLabel: {
                    textStyle: {
                        color: "rgba(255,255,255,.6)",
                        fontSize: 14,
                    },
                },
                axisLine: {
                    lineStyle: {
                        color: 'rgba(255,255,255,.1)'
                    }

                },

                data: timelist,

            }, {

                axisPointer: {show: false},
                axisLine: {show: false},
                position: 'bottom',
                offset: 20,


            }],

            yAxis: [{
                type: 'value',
                axisTick: {show: false},
                // splitNumber: 6,
                max: function (value) {
                    return Math.floor(value.max) + 20;
                },
                min: function (value) {
                    return Math.floor(value.min);
                },
                axisLine: {
                    lineStyle: {
                        color: 'rgba(255,255,255,.1)'
                    }
                },
                axisLabel: {
                    textStyle: {
                        color: "rgba(255,255,255,.6)",
                        fontSize: 14,
                    },
                },

                splitLine: {
                    lineStyle: {
                        color: 'rgba(255,255,255,.1)'
                    }
                }
            }],
            series: [
                {
                    name: 'BTC',
                    type: 'line',
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 5,
                    showSymbol: false,
                    lineStyle: {

                        normal: {
                            color: 'rgba(228, 228, 126, 1)',
                            width: 2
                        }
                    },
                    areaStyle: {
                        normal: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                offset: 0,
                                color: 'rgba(228, 228, 126, .8)'
                            }, {
                                offset: 0.8,
                                color: 'rgba(228, 228, 126, 0.1)'
                            }], false),
                            shadowColor: 'rgba(0, 0, 0, 0.1)',
                        }
                    },
                    itemStyle: {
                        normal: {
                            color: '#dddc6b',
                            borderColor: 'rgba(221, 220, 107, .1)',
                            borderWidth: 12
                        }
                    },
                    data: bitcoin_price,
                },
                {
                    name: 'ETH',
                    type: 'line',
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 5,
                    showSymbol: false,
                    lineStyle: {

                        normal: {
                            color: 'rgba(255, 128, 128, 1)',
                            width: 2
                        }
                    },
                    areaStyle: {
                        normal: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                offset: 0,
                                color: 'rgba(255, 128, 128,.8)'
                            }, {
                                offset: 0.8,
                                color: 'rgba(255, 128, 128, .1)'
                            }], false),
                            shadowColor: 'rgba(0, 0, 0, 0.1)',
                        }
                    },
                    itemStyle: {
                        normal: {
                            color: 'rgba(255, 128, 128,.8)',
                            borderColor: 'rgba(221, 220, 107, .1)',
                            borderWidth: 12
                        }
                    },
                    data: ethereum_price,

                },
                {
                    name: 'MKR',
                    type: 'line',
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 5,
                    showSymbol: false,
                    lineStyle: {

                        normal: {
                            color: 'rgba(150, 255, 153, 1)',
                            width: 2
                        }
                    },
                    areaStyle: {
                        normal: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                offset: 0,
                                color: 'rgba(228, 228, 126, .8)'
                            }, {
                                offset: 0.8,
                                color: 'rgba(228, 228, 126, 0.1)'
                            }], false),
                            shadowColor: 'rgba(0, 0, 0, 0.1)',
                        }
                    },
                    itemStyle: {
                        normal: {
                            color: 'rgba(150, 255, 153, 1)',
                            borderColor: 'rgba(221, 220, 107, .1)',
                            borderWidth: 12
                        }
                    },
                    data: tether_price,
                },

            ]

        };

        // 使用刚指定的配置项和数据显示图表。
        myChart2.setOption(option);
        window.addEventListener("resize", function () {
            myChart2.resize();
        });
    });

    // // 基于准备好的dom，初始化echarts实例
    // var myChart = echarts.init(document.querySelector(".line1 .chart"));
    //
    // option = {
    //     tooltip: {
    //         trigger: "axis",
    //         axisPointer: {
    //             lineStyle: {
    //                 color: "#dddc6b"
    //             }
    //         }
    //     },
    //     legend: {
    //         top: "0%",
    //         textStyle: {
    //             color: "rgba(255,255,255,.5)",
    //             fontSize: "12"
    //         }
    //     },
    //     grid: {
    //         left: "10",
    //         top: "30",
    //         right: "10",
    //         bottom: "10",
    //         containLabel: true
    //     },
    //
    //     xAxis: [
    //         {
    //             type: "category",
    //             boundaryGap: false,
    //             axisLabel: {
    //                 textStyle: {
    //                     color: "rgba(255,255,255,.6)",
    //                     fontSize: 12
    //                 }
    //             },
    //             axisLine: {
    //                 lineStyle: {
    //                     color: "rgba(255,255,255,.2)"
    //                 }
    //             },
    //
    //             data: [
    //                 "01",
    //                 "02",
    //                 "03",
    //                 "04",
    //                 "05",
    //                 "06",
    //                 "07",
    //                 "08",
    //                 "09",
    //                 "11",
    //                 "12",
    //                 "13",
    //                 "14",
    //                 "15",
    //                 "16",
    //                 "17",
    //                 "18",
    //                 "19",
    //                 "20",
    //                 "21",
    //                 "22",
    //                 "23",
    //                 "24",
    //                 "25",
    //                 "26",
    //                 "27",
    //                 "28",
    //                 "29",
    //                 "30"
    //             ]
    //         },
    //         {
    //             axisPointer: {show: false},
    //             axisLine: {show: false},
    //             position: "bottom",
    //             offset: 20
    //         }
    //     ],
    //
    //     yAxis: [
    //         {
    //             type: "value",
    //             axisTick: {show: false},
    //             axisLine: {
    //                 lineStyle: {
    //                     color: "rgba(255,255,255,.1)"
    //                 }
    //             },
    //             axisLabel: {
    //                 textStyle: {
    //                     color: "rgba(255,255,255,.6)",
    //                     fontSize: 12
    //                 }
    //             },
    //
    //             splitLine: {
    //                 lineStyle: {
    //                     color: "rgba(255,255,255,.1)"
    //                 }
    //             }
    //         }
    //     ],
    //     series: [
    //         {
    //             name: "流入",
    //             type: "line",
    //             smooth: true,
    //             symbol: "circle",
    //             symbolSize: 5,
    //             showSymbol: false,
    //             lineStyle: {
    //                 normal: {
    //                     color: "#0184d5",
    //                     width: 2
    //                 }
    //             },
    //             areaStyle: {
    //                 normal: {
    //                     color: new echarts.graphic.LinearGradient(
    //                         0,
    //                         0,
    //                         0,
    //                         1,
    //                         [
    //                             {
    //                                 offset: 0,
    //                                 color: "rgba(1, 132, 213, 0.4)"
    //                             },
    //                             {
    //                                 offset: 0.8,
    //                                 color: "rgba(1, 132, 213, 0.1)"
    //                             }
    //                         ],
    //                         false
    //                     ),
    //                     shadowColor: "rgba(0, 0, 0, 0.1)"
    //                 }
    //             },
    //             itemStyle: {
    //                 normal: {
    //                     color: "#0184d5",
    //                     borderColor: "rgba(221, 220, 107, .1)",
    //                     borderWidth: 12
    //                 }
    //             },
    //             data: [
    //                 30,
    //                 40,
    //                 30,
    //                 40,
    //                 30,
    //                 40,
    //                 30,
    //                 60,
    //                 20,
    //                 40,
    //                 20,
    //                 40,
    //                 30,
    //                 40,
    //                 30,
    //                 40,
    //                 30,
    //                 40,
    //                 30,
    //                 60,
    //                 20,
    //                 40,
    //                 20,
    //                 40,
    //                 30,
    //                 60,
    //                 20,
    //                 40,
    //                 20,
    //                 40
    //             ]
    //         },
    //         {
    //             name: "流出",
    //             type: "line",
    //             smooth: true,
    //             symbol: "circle",
    //             symbolSize: 5,
    //             showSymbol: false,
    //             lineStyle: {
    //                 normal: {
    //                     color: "#00d887",
    //                     width: 2
    //                 }
    //             },
    //             areaStyle: {
    //                 normal: {
    //                     color: new echarts.graphic.LinearGradient(
    //                         0,
    //                         0,
    //                         0,
    //                         1,
    //                         [
    //                             {
    //                                 offset: 0,
    //                                 color: "rgba(0, 216, 135, 0.4)"
    //                             },
    //                             {
    //                                 offset: 0.8,
    //                                 color: "rgba(0, 216, 135, 0.1)"
    //                             }
    //                         ],
    //                         false
    //                     ),
    //                     shadowColor: "rgba(0, 0, 0, 0.1)"
    //                 }
    //             },
    //             itemStyle: {
    //                 normal: {
    //                     color: "#00d887",
    //                     borderColor: "rgba(221, 220, 107, .1)",
    //                     borderWidth: 12
    //                 }
    //             },
    //             data: [
    //                 50,
    //                 30,
    //                 50,
    //                 60,
    //                 10,
    //                 50,
    //                 30,
    //                 50,
    //                 60,
    //                 40,
    //                 60,
    //                 40,
    //                 80,
    //                 30,
    //                 50,
    //                 60,
    //                 10,
    //                 50,
    //                 30,
    //                 70,
    //                 20,
    //                 50,
    //                 10,
    //                 40,
    //                 50,
    //                 30,
    //                 70,
    //                 20,
    //                 50,
    //                 10,
    //                 40
    //             ]
    //         }
    //     ]
    // };
    //
    // // 使用刚指定的配置项和数据显示图表。
    // myChart.setOption(option);
    // window.addEventListener("resize", function () {
    //     myChart.resize();
    // });

})();

// 交易所交易额占比
(function () {
    var data_dict = {}
    var data_json = []
    for(var i=0;i<exchange_name_list.length;i++){
        data_dict = {
          "value":exchange_volumeUsd[i],
          "name":exchange_name_list[i],
        };
        data_json.push(data_dict)
    }
    // console.log(data_json)
    // 1. 实例化对象
    var myChart = echarts.init(document.querySelector(".pie1  .chart"));
    // 2. 指定配置项和数据
    var option = {
        legend: {
            top: "90%",
            itemWidth: 10,
            itemHeight: 10,
            textStyle: {
                color: "rgba(255,255,255,.5)",
                fontSize: "12"
            }
        },
        tooltip: {
            trigger: "item",
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        // 注意颜色写的位置
        color: [
            "#006cff",
            "#60cda0",
            "#ed8884",
            "#ff9f7f",
            "#0096ff",
            "#9fe6b8",
            "#32c5e9",
            "#1d9dff"
        ],
        series: [
            {
                name: "点位统计",
                type: "pie",
                // 如果radius是百分比则必须加引号
                radius: ["10%", "70%"],
                center: ["50%", "42%"],
                roseType: "radius",
                // data: [
                //     {value: 20, name: "西安"},
                //     {value: 26, name: "北京"},
                //     {value: 24, name: "上海"},
                //     {value: 25, name: "其他"},
                //     {value: 20, name: "武汉"},
                //     {value: 25, name: "杭州"},
                //     {value: 30, name: "深圳"},
                //     {value: 42, name: "广州"}
                // ],
                data:data_json,
                // 修饰饼形图文字相关的样式 label对象
                label: {
                    fontSize: 10
                },
                // 修饰引导线样式
                labelLine: {
                    // 连接到图形的线长度
                    length: 10,
                    // 连接到文字的线长度
                    length2: 10
                }
            }
        ]
    };

    // 3. 配置项和数据给我们的实例化对象
    myChart.setOption(option);
    // 4. 当我们浏览器缩放的时候，图表也等比例缩放
    window.addEventListener("resize", function () {
        // 让我们的图表调用 resize这个方法
        myChart.resize();
    });
})();
