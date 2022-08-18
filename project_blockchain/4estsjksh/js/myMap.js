(function () {

    // 基于准备好的dom，初始化echarts实例
    // var myChart = echarts.init(document.getElementById('lastecharts'));
    var myChart = echarts.init(document.querySelector(".map .chart"));
    var uploadedDataURL = "./data-1528971808162-BkOXf61WX.json";
    $.ajax({
        url: 'http://127.0.0.1:8000/map_data2',
        type: 'get',
        dataType: 'json',
        async: false,
        success: function (data) {
            map_data = data;
        }
    })
    var height = map_data.data.height;
    var height_set=document.getElementById("height");
    height_set.innerHTML=height;
    var point_list = map_data.data.point_list;
    var point_dict = {};
    for (var i = 0; i < point_list.length; i++) {
        point_dict[i] =point_list[i];
    }

    var colorIndex = 0;
    var geoCoordMap = {
        '1':[118.7,34.48],
        '2':[114.7,35.83],

        // 吉林: [[13950002.65, 5419815.34], [12959219.6, 4825334.63]],
        // 吉林: [126.4746, 43.5938],
        //
        // // 吉林: '126.4746, 43.5938',
        // 北京: [116.4551, 40.2539],    //修改
        // // 北京:[],
        // // 北京1:[117.4551,40.2539],    //修改
        // // 北京:[129.5921,482,5334],
        // // 北京: [135.2411, 36.4278],
        // 天津: [117.4219, 39.4189],
        // 河北: [114.4995, 38.1006],
        // 山西: [112.3352, 37.9413],
        // 内蒙古: [110.3467, 41.4899],
        // 辽宁: [123.1238, 42.1216],
        // 吉林: [125.8154, 44.2584],
        // // 黑龙江: [127.9688, 45.368],
        // '': [129.5921, 48.2533,],
        // 上海: [121.4648, 31.2891],
        // // 上海:[135.2411, 36.4278],
        // 江苏: [118.8062, 31.9208],
        // 安徽: [117.29, 32.0581],
        // 浙江: [119.5313, 29.8773],
        // 福建: [119.4543, 25.9222],
        // 江西: [116.0046, 28.6633],
        // 山东: [117.1582, 36.8701],
        // 河南: [113.4668, 34.6234],
        // 湖北: [114.3896, 30.6628],
        // 湖南: [113.0823, 28.2568],
        // 广东: [113.12244, 23.009505],
        // 广西: [108.479, 23.1152],
        // 海南: [110.3893, 19.8516],
        // 重庆: [108.384366, 30.439702],
        // 四川: [103.9526, 30.7617],
        // 贵州: [106.6992, 26.7682],
        // 云南: [102.9199, 25.4663],
        // 陕西: [109.1162, 34.2004],
        // 甘肃: [103.5901, 36.3043],
        // 青海: [101.4038, 36.8207],
        // 宁夏: [106.3586, 38.1775],
        // // 新疆: [87.9236, 43.5883],
        // 新疆: [80.9236, 43.5883],
        西藏: [91.11, 29.97],
        'sad':[126.2319, 26.643],
        'aa':[113.39481756,23.40800373]
    };
    var geoCoordMap = point_dict
    // var voltageLevel = ['722560', '722561', '722562', '722563', '722564'];
    var voltageLevel = ['722560'];
    // console.log(height_arr)
    // var voltageLevel = height_arr_reverse;  //页面地图下面的横线选项数据
    var mapData = [[], [], [], [], []];

    //左边的条形图数据
    // var line_one = city_list_change_one;
    // var line_two = city_list_change_two;
    // var line_three = city_list_change_three;
    // var line_four = city_list_change_four;
    // var line_five = city_list_change_five;


    var line_three = {
        北京: 69.5,
        天津: 68.4,
        河北: 67.3,
        山西: 50.4,
        内蒙古: 21.8,
        辽宁: 37.8,
        吉林: 32.8,
        黑龙江: 25.3,
        上海: 43.3,
        江苏: 50.2,
        浙江: 35.7,
        安徽: 52.9,
        福建: 24.3,
        江西: 37.3,
        山东: 61.3,
        河南: 65.7,
        湖北: 50.5,
        湖南: 43.6,
        广东: 28.6,
        广西: 32.2,
        海南: 15.9,
        重庆: 45.2,
        四川: 44.3,
        贵州: 30.9,
        云南: 21.4,
        陕西: 51.1,
        甘肃: 39.8,
        青海: 28.5,
        宁夏: 40.3,
        新疆: 53.8,
        西藏: 7.6,
    };
    var line_four = {
        北京: 55.7,
        天津: 60.1,
        河北: 60.1,
        山西: 49.4,
        内蒙古: 22.5,
        辽宁: 36.8,
        吉林: 36.9,
        黑龙江: 32.3,
        上海: 39.1,
        江苏: 48.3,
        浙江: 35.4,
        安徽: 56,
        福建: 24,
        江西: 38.5,
        山东: 54.3,
        河南: 61,
        湖北: 48.5,
        湖南: 41.4,
        广东: 29.9,
        广西: 31.7,
        海南: 15.8,
        重庆: 38.5,
        四川: 40.5,
        贵州: 27.8,
        云南: 18.1,
        陕西: 50.2,
        甘肃: 34.5,
        青海: 25.6,
        宁夏: 35.6,
        新疆: 49.7,
        西藏: 5.7,
    };
    var line_five = {
        北京: 0,
        天津: 0,
        河北: 2,
        山西: 0,
        内蒙古: 0,
        辽宁: 31.6,
        吉林: 26.7,
        黑龙江: 23.3,
        上海: 35.7,
        江苏: 46.2,
        浙江: 30.6,
        安徽: 49.9,
        福建: 22.2,
        江西: 31.4,
        山东: 47.7,
        河南: 57.3,
        湖北: 43.2,
        湖南: 37,
        广东: 27,
        广西: 29.2,
        海南: 15.7,
        重庆: 33.4,
        四川: 36.3,
        贵州: 24.8,
        云南: 17.8,
        陕西: 44.2,
        甘肃: 32.7,
        青海: 25.9,
        宁夏: 33,
        新疆: 53.5,
        西藏: 5.8,

    };

    // var d2018 = city_list_change_one;
    // var d2017 = city_list_change_two;
    // var d2016 = city_dict_three;

    var line_one = {
        '': 33,
        '': 88,
        北京1: 80,
        北京: 78.5,
        天津: 70.6,
        河北: 74.8,
        山西: 50.7,
        内蒙古: 24.8,
        辽宁: 49,
        吉林: 45.8,
        黑龙江: 80.9,
        上海: 51.9,
        江苏: 58.6,
        浙江: 41.9,
        安徽: 58.9,
        福建: 25.6,
        江西: 37.6,
        山东: 69.7,
        河南: 73.7,
        湖北: 57.8,
        湖南: 47.9,
        广东: 30.7,
        广西: 35.4,
        海南: 15.9,
        重庆: 46.2,
        四川: 45,
        贵州: 32.6,
        云南: 20.9,
        陕西: 47,
        甘肃: 38.7,
        青海: 29.2,
        宁夏: 39.4,
        新疆: 49.2,
        西藏: 6.7,
    };

    var line_two = {
        北京: 79.5,
        天津: 84.1,
        河北: 82.4,
        山西: 56.4,
        内蒙古: 26.1,
        辽宁: 49.2,
        吉林: 48.6,
        黑龙江: 40.1,
        上海: 49.6,
        江苏: 62.5,
        浙江: 46.8,
        安徽: 68,
        福建: 28.6,
        江西: 44.4,
        山东: 71.2,
        河南: 77.2,
        湖北: 64.5,
        湖南: 57.2,
        广东: 35.6,
        广西: 40.3,
        海南: 16.6,
        重庆: 53.1,
        四川: 54.3,
        贵州: 36,
        云南: 22.7,
        陕西: 54.3,
        甘肃: 43,
        青海: 35.9,
        宁夏: 40.1,
        新疆: 59.1,
        西藏: 7.7,
    };

    var colors = [
        ['#1DE9B6', '#F46E36', '#04B9FF', '#5DBD32', '#FFC809', '#FB95D5', '#BDA29A', '#6E7074', '#546570', '#C4CCD3'],
        [
            '#37A2DA',
            '#67E0E3',
            '#32C5E9',
            '#9FE6B8',
            '#FFDB5C',
            '#FF9F7F',
            '#FB7293',
            '#E062AE',
            '#E690D1',
            '#E7BCF3',
            '#9D96F5',
            '#8378EA',
            '#8378EA',
        ],
        [
            '#DD6B66',
            '#759AA0',
            '#E69D87',
            '#8DC1A9',
            '#EA7E53',
            '#EEDD78',
            '#73A373',
            '#73B9BC',
            '#7289AB',
            '#91CA8C',
            '#F49F42',
        ],
    ];


    var categoryData = [];
    var barData = [];
    for (var key in geoCoordMap) {
        categoryData.push(key);
        mapData[0].push({
            year: '2014',
            name: key,
            // value: line_one[key],
            value: geoCoordMap[key],
        });

        // mapData[1].push({
        //     year: '20154',
        //     name: key,
        //     value: line_two[key],
        // });
        // mapData[2].push({
        //     year: '2016',
        //     name: key,
        //     value: line_three[key],
        // });
        // mapData[3].push({
        //     year: '2017',
        //     name: key,
        //     value: line_four[key],
        // });
        // mapData[4].push({
        //     year: '2018',
        //     name: key,
        //     value: line_five[key],
        // });
    }

    for (var i = 0; i < mapData.length; i++) {
        barData.push([]);
        for (var j = 0; j < mapData[i].length; j++) {
            barData[i].push(mapData[i][j].value);
        }
    }
    $.getJSON(uploadedDataURL, function (geoJson) {
        echarts.registerMap('china', geoJson);
        var convertData = function (data) {
            var res = [];
            for (var i = 0; i < data.length; i++) {
                var geoCoord = geoCoordMap[data[i].name];
                if (geoCoord) {
                    res.push({
                        name: data[i].name,
                        value: geoCoord.concat(data[i].value),
                    });
                }
            }
            return res;
        };

        var convertToLineData = function (data) {
            var res = [];
            for (var i = 0; i < data.length; i++) {
                var dataItem = data[i];
                var fromCoord = geoCoordMap[dataItem.name];
                var toCoord = gps; //市区
                if (fromCoord && toCoord) {
                    res.push([
                        {
                            coord: fromCoord,
                            value: dataItem.value,
                        },
                        {
                            coord: toCoord,
                        },
                    ]);
                }
            }
            return res;
        };

        let optionXyMap01 = {
            timeline: {
                data: voltageLevel,
                axisType: 'category',
                autoPlay: true,
                show: false,   //修改。
                playInterval: 3000,
                left: '3%',
                right: '10%',
                bottom: '3%',
                width: '70%',
                //  height: null,
                label: {
                    normal: {
                        textStyle: {
                            color: '#ddd',
                        },
                    },
                    emphasis: {
                        textStyle: {
                            color: '#fff',
                        },
                    },
                },
                symbolSize: 10,
                lineStyle: {
                    color: '#555',
                },
                checkpointStyle: {
                    borderColor: '#888',
                    borderWidth: 2,
                },
                controlStyle: {
                    showNextBtn: true,
                    showPrevBtn: true,
                    normal: {
                        color: '#666',
                        borderColor: '#666',
                    },
                    emphasis: {
                        color: '#aaa',
                        borderColor: '#aaa',
                    },
                },
            },
            baseOption: {
                animation: true,
                animationDuration: 1000,
                animationEasing: 'cubicInOut',
                animationDurationUpdate: 1000,
                animationEasingUpdate: 'cubicInOut',
                grid: {
                    right: '1%',
                    top: '15%',
                    bottom: '2%',
                    width: '20%',
                },
                tooltip: {
                    trigger: 'axis', // hover触发器
                    axisPointer: {
                        // 坐标轴指示器，坐标轴触发有效
                        type: 'shadow', // 默认为直线，可选为：'line' | 'shadow'
                        shadowStyle: {
                            color: 'rgba(150,150,150,0.1)', //hover颜色
                        },
                    },
                },
                geo: {
                    show: true,
                    map: 'china',
                    left: 120,     //修改
                    roam: true,
                    zoom: 1,
                    center: [113.83531246, 34.0267395887], //中心点
                    label: {
                        emphasis: {
                            show: false,
                        },
                    },
                    itemStyle: {
                        normal: {
                            borderColor: 'rgba(147, 235, 248, 1)',
                            borderWidth: 1,
                            areaColor: {
                                type: 'radial',
                                x: 0.5,
                                y: 0.5,
                                r: 0.5,
                                colorStops: [
                                    {
                                        offset: 0,
                                        color: 'rgba(147, 235, 248, 0)', // 0% 处的颜色
                                    },
                                    {
                                        offset: 1,
                                        color: 'rgba(147, 235, 248, .2)', // 100% 处的颜色
                                    },
                                ],
                                globalCoord: false, // 缺省为 false
                            },
                            // shadowColor: 'rgba(128, 217, 248, 1)',
                            // shadowColor: 'rgba(255, 255, 255, 1)',
                            // shadowOffsetX: -2,
                            // shadowOffsetY: 2,
                            // shadowBlur: 10
                        },
                        emphasis: {
                            areaColor: '#389BB7',
                            borderWidth: 0,
                        },
                    },
                },
            },
            options: [],
        };
        for (var n = 0; n < voltageLevel.length; n++) {
            optionXyMap01.options.push({
                // backgroundColor: '#142037',

                title: [
                    {
                        //text: '最新节点区域监控',
                        left: '15%',
                        top: '1%',
                        textStyle: {
                            color: '#EEDD78',
                            fontSize: 30,
                        },
                    },
                    {
                        id: 'statistic',
                        text: voltageLevel[n] + '区块情况',
                        show: false,
                        left: '70%',
                        top: '3%',
                        textStyle: {
                            color: '#EEDD78',
                            fontSize: 20,
                        },
                    },
                ],
                xAxis: {
                    type: 'value',
                    show: false,
                    scale: true,
                    position: 'top',
                    min: 0,
                    // max:15,
                    boundaryGap: false,
                    splitLine: {
                        show: false,
                    },
                    axisLine: {
                        show: false,
                    },
                    axisTick: {
                        show: false,
                    },
                    axisLabel: {
                        margin: 2,
                        textStyle: {
                            color: '#aaa',
                        },
                    },
                },
                yAxis: {
                    type: 'category',
                    //  name: 'TOP 20',
                    show: false,   //修改
                    nameGap: 16,
                    axisLine: {
                        show: true,
                        lineStyle: {
                            color: '#ddd',
                        },
                    },
                    axisTick: {
                        show: false,
                        lineStyle: {
                            color: '#ddd',
                        },
                    },
                    axisLabel: {
                        interval: 0,
                        textStyle: {
                            color: '#ddd',
                        },
                    },
                    // data: categoryData,    //修改
                },
                series: [
                    {
                        //文字和标志
                        name: 'light',
                        type: 'scatter',
                        coordinateSystem: 'geo',
                        data: convertData(mapData[n]),
                        symbolSize: function (val) {
                            // return (val[2]) / 1;
                            return (val[2]) / 20; //修改点的大小
                            // return 6.5
                        },

                        itemStyle: {
                            normal: {
                                color: colors[colorIndex][n],
                            },
                        },
                    },
                    {
                        type: 'map',
                        map: 'china',

                        geoIndex: 0,
                        aspectScale: 0.75, //长宽比
                        showLegendSymbol: false, // 存在legend时显示
                        label: {
                            normal: {
                                show: false,
                            },
                            emphasis: {
                                show: false,
                                textStyle: {
                                    color: '#fff',
                                },
                            },
                        },
                        roam: true,
                        itemStyle: {
                            normal: {

                                areaColor: '#031525',
                                borderColor: '#FFFFFF',
                            },
                            emphasis: {
                                areaColor: '#2B91B7',
                            },
                        },
                        animation: false,
                        data: mapData,
                    },
                    {
                        //  name: 'Top 10',
                        type: 'effectScatter',

                        coordinateSystem: 'geo',
                        data: convertData(
                            mapData[n]
                                .sort(function (a, b) {
                                    return b.value - a.value;
                                })
                                .slice(0, 20)
                        ),
                        symbolSize: function (val) {
                            // return (val[2]) / 10;
                            return 6.5;       //修改
                        },
                        showEffectOn: 'render',
                        rippleEffect: {
                            brushType: 'stroke',
                        },
                        hoverAnimation: true,
                        label: {
                            normal: {
                                show: false, //修改
                                // show: true,
                                formatter: '{b}',
                                position: 'right',
                            },
                        },
                        itemStyle: {
                            normal: {

                                color: colors[colorIndex][n],
                                shadowBlur: 5,
                                shadowColor: colors[colorIndex][n],
                            },
                        },
                        zlevel: 1,
                    },

                    {
                        zlevel: 1.5,
                        type: 'bar',
                        symbol: 'none',
                        itemStyle: {
                            normal: {

                                color: colors[colorIndex][n],
                            },
                        },
                        // data: barData[n],  //修改
                    },
                ],
            });
        }
        myChart.setOption(optionXyMap01);
        window.addEventListener("resize", function () {
            myChart.resize();
        });
    });


    // 1. 实例化对象
    // var myChart = echarts.init(document.querySelector(".map .chart"));
    // // 2. 指定配置和数据
    // // 2. 指定配置和数据
    // var geoCoordMap = {
    //   上海: [121.4648, 31.2891],
    //   东莞: [113.8953, 22.901],
    //   东营: [118.7073, 37.5513],
    //   中山: [113.4229, 22.478],
    //   临汾: [111.4783, 36.1615],
    //   临沂: [118.3118, 35.2936],
    //   丹东: [124.541, 40.4242],
    //   丽水: [119.5642, 28.1854],
    //   乌鲁木齐: [87.9236, 43.5883],
    //   佛山: [112.8955, 23.1097],
    //   保定: [115.0488, 39.0948],
    //   兰州: [103.5901, 36.3043],
    //   包头: [110.3467, 41.4899],
    //   北京: [116.4551, 40.2539],
    //   北海: [109.314, 21.6211],
    //   南京: [118.8062, 31.9208],
    //   南宁: [108.479, 23.1152],
    //   南昌: [116.0046, 28.6633],
    //   南通: [121.1023, 32.1625],
    //   厦门: [118.1689, 24.6478],
    //   台州: [121.1353, 28.6688],
    //   合肥: [117.29, 32.0581],
    //   呼和浩特: [111.4124, 40.4901],
    //   咸阳: [108.4131, 34.8706],
    //   哈尔滨: [127.9688, 45.368],
    //   唐山: [118.4766, 39.6826],
    //   嘉兴: [120.9155, 30.6354],
    //   大同: [113.7854, 39.8035],
    //   大连: [122.2229, 39.4409],
    //   天津: [117.4219, 39.4189],
    //   太原: [112.3352, 37.9413],
    //   威海: [121.9482, 37.1393],
    //   宁波: [121.5967, 29.6466],
    //   宝鸡: [107.1826, 34.3433],
    //   宿迁: [118.5535, 33.7775],
    //   常州: [119.4543, 31.5582],
    //   广州: [113.5107, 23.2196],
    //   廊坊: [116.521, 39.0509],
    //   延安: [109.1052, 36.4252],
    //   张家口: [115.1477, 40.8527],
    //   徐州: [117.5208, 34.3268],
    //   德州: [116.6858, 37.2107],
    //   惠州: [114.6204, 23.1647],
    //   成都: [103.9526, 30.7617],
    //   扬州: [119.4653, 32.8162],
    //   承德: [117.5757, 41.4075],
    //   拉萨: [91.1865, 30.1465],
    //   无锡: [120.3442, 31.5527],
    //   日照: [119.2786, 35.5023],
    //   昆明: [102.9199, 25.4663],
    //   杭州: [119.5313, 29.8773],
    //   枣庄: [117.323, 34.8926],
    //   柳州: [109.3799, 24.9774],
    //   株洲: [113.5327, 27.0319],
    //   武汉: [114.3896, 30.6628],
    //   汕头: [117.1692, 23.3405],
    //   江门: [112.6318, 22.1484],
    //   沈阳: [123.1238, 42.1216],
    //   沧州: [116.8286, 38.2104],
    //   河源: [114.917, 23.9722],
    //   泉州: [118.3228, 25.1147],
    //   泰安: [117.0264, 36.0516],
    //   泰州: [120.0586, 32.5525],
    //   济南: [117.1582, 36.8701],
    //   济宁: [116.8286, 35.3375],
    //   海口: [110.3893, 19.8516],
    //   淄博: [118.0371, 36.6064],
    //   淮安: [118.927, 33.4039],
    //   深圳: [114.5435, 22.5439],
    //   清远: [112.9175, 24.3292],
    //   温州: [120.498, 27.8119],
    //   渭南: [109.7864, 35.0299],
    //   湖州: [119.8608, 30.7782],
    //   湘潭: [112.5439, 27.7075],
    //   滨州: [117.8174, 37.4963],
    //   潍坊: [119.0918, 36.524],
    //   烟台: [120.7397, 37.5128],
    //   玉溪: [101.9312, 23.8898],
    //   珠海: [113.7305, 22.1155],
    //   盐城: [120.2234, 33.5577],
    //   盘锦: [121.9482, 41.0449],
    //   石家庄: [114.4995, 38.1006],
    //   福州: [119.4543, 25.9222],
    //   秦皇岛: [119.2126, 40.0232],
    //   绍兴: [120.564, 29.7565],
    //   聊城: [115.9167, 36.4032],
    //   肇庆: [112.1265, 23.5822],
    //   舟山: [122.2559, 30.2234],
    //   苏州: [120.6519, 31.3989],
    //   莱芜: [117.6526, 36.2714],
    //   菏泽: [115.6201, 35.2057],
    //   营口: [122.4316, 40.4297],
    //   葫芦岛: [120.1575, 40.578],
    //   衡水: [115.8838, 37.7161],
    //   衢州: [118.6853, 28.8666],
    //   西宁: [101.4038, 36.8207],
    //   西安: [109.1162, 34.2004],
    //   贵阳: [106.6992, 26.7682],
    //   连云港: [119.1248, 34.552],
    //   邢台: [114.8071, 37.2821],
    //   邯郸: [114.4775, 36.535],
    //   郑州: [113.4668, 34.6234],
    //   鄂尔多斯: [108.9734, 39.2487],
    //   重庆: [107.7539, 30.1904],
    //   金华: [120.0037, 29.1028],
    //   铜川: [109.0393, 35.1947],
    //   银川: [106.3586, 38.1775],
    //   镇江: [119.4763, 31.9702],
    //   长春: [125.8154, 44.2584],
    //   长沙: [113.0823, 28.2568],
    //   长治: [112.8625, 36.4746],
    //   阳泉: [113.4778, 38.0951],
    //   青岛: [120.4651, 36.3373],
    //   韶关: [113.7964, 24.7028]
    // };
    //
    // var XAData = [
    //   [{ name: "西安" }, { name: "北京", value: 100 }],
    //   [{ name: "西安" }, { name: "上海", value: 100 }],
    //   [{ name: "西安" }, { name: "广州", value: 100 }],
    //   [{ name: "西安" }, { name: "西宁", value: 100 }],
    //   [{ name: "西安" }, { name: "拉萨", value: 100 }]
    // ];
    //
    // var XNData = [
    //   [{ name: "西宁" }, { name: "北京", value: 100 }],
    //   [{ name: "西宁" }, { name: "上海", value: 100 }],
    //   [{ name: "西宁" }, { name: "广州", value: 100 }],
    //   [{ name: "西宁" }, { name: "西安", value: 100 }],
    //   [{ name: "西宁" }, { name: "银川", value: 100 }]
    // ];
    //
    // var YCData = [
    //   [{ name: "拉萨" }, { name: "北京", value: 100 }],
    //   [{ name: "拉萨" }, { name: "潍坊", value: 100 }],
    //   [{ name: "拉萨" }, { name: "哈尔滨", value: 100 }]
    // ];
    //
    // var planePath =
    //   "path://M1705.06,1318.313v-89.254l-319.9-221.799l0.073-208.063c0.521-84.662-26.629-121.796-63.961-121.491c-37.332-0.305-64.482,36.829-63.961,121.491l0.073,208.063l-319.9,221.799v89.254l330.343-157.288l12.238,241.308l-134.449,92.931l0.531,42.034l175.125-42.917l175.125,42.917l0.531-42.034l-134.449-92.931l12.238-241.308L1705.06,1318.313z";
    // //var planePath = 'arrow';
    // var convertData = function(data) {
    //   var res = [];
    //   for (var i = 0; i < data.length; i++) {
    //     var dataItem = data[i];
    //
    //     var fromCoord = geoCoordMap[dataItem[0].name];
    //     var toCoord = geoCoordMap[dataItem[1].name];
    //     if (fromCoord && toCoord) {
    //       res.push({
    //         fromName: dataItem[0].name,
    //         toName: dataItem[1].name,
    //         coords: [fromCoord, toCoord],
    //         value: dataItem[1].value
    //       });
    //     }
    //   }
    //   return res;
    // };
    //
    // var color = ["#fff", "#fff", "#fff"]; //航线的颜色
    // var series = [];
    // [
    //   ["西安", XAData],
    //   ["西宁", XNData],
    //   ["银川", YCData]
    // ].forEach(function(item, i) {
    //   series.push(
    //     {
    //       name: item[0] + " Top3",
    //       type: "lines",
    //       zlevel: 1,
    //       effect: {
    //         show: true,
    //         period: 6,
    //         trailLength: 0.7,
    //         color: "red", //arrow箭头的颜色
    //         symbolSize: 3
    //       },
    //       lineStyle: {
    //         normal: {
    //           color: color[i],
    //           width: 0,
    //           curveness: 0.2
    //         }
    //       },
    //       data: convertData(item[1])
    //     },
    //     {
    //       name: item[0] + " Top3",
    //       type: "lines",
    //       zlevel: 2,
    //       symbol: ["none", "arrow"],
    //       symbolSize: 10,
    //       effect: {
    //         show: true,
    //         period: 6,
    //         trailLength: 0,
    //         symbol: planePath,
    //         symbolSize: 15
    //       },
    //       lineStyle: {
    //         normal: {
    //           color: color[i],
    //           width: 1,
    //           opacity: 0.6,
    //           curveness: 0.2
    //         }
    //       },
    //       data: convertData(item[1])
    //     },
    //     {
    //       name: item[0] + " Top3",
    //       type: "effectScatter",
    //       coordinateSystem: "geo",
    //       zlevel: 2,
    //       rippleEffect: {
    //         brushType: "stroke"
    //       },
    //       label: {
    //         normal: {
    //           show: true,
    //           position: "right",
    //           formatter: "{b}"
    //         }
    //       },
    //       symbolSize: function(val) {
    //         return val[2] / 8;
    //       },
    //       itemStyle: {
    //         normal: {
    //           color: color[i]
    //         },
    //         emphasis: {
    //           areaColor: "#2B91B7"
    //         }
    //       },
    //       data: item[1].map(function(dataItem) {
    //         return {
    //           name: dataItem[1].name,
    //           value: geoCoordMap[dataItem[1].name].concat([dataItem[1].value])
    //         };
    //       })
    //     }
    //   );
    // });
    // var option = {
    //   tooltip: {
    //     trigger: "item",
    //     formatter: function(params, ticket, callback) {
    //       if (params.seriesType == "effectScatter") {
    //         return "线路：" + params.data.name + "" + params.data.value[2];
    //       } else if (params.seriesType == "lines") {
    //         return (
    //           params.data.fromName +
    //           ">" +
    //           params.data.toName +
    //           "<br />" +
    //           params.data.value
    //         );
    //       } else {
    //         return params.name;
    //       }
    //     }
    //   },
    //
    //   geo: {
    //     map: "china",
    //     label: {
    //       emphasis: {
    //         show: true,
    //         color: "#fff"
    //       }
    //     },
    //     roam: false,
    //     //   放大我们的地图
    //     zoom: 1,
    //     itemStyle: {
    //       normal: {
    //         areaColor: "rgba(43, 196, 243, 0.42)",
    //         borderColor: "rgba(43, 196, 243, 1)",
    //         borderWidth: 1
    //       },
    //       emphasis: {
    //         areaColor: "#2B91B7"
    //       }
    //     }
    //   },
    //   series: series
    // };
    // myChart.setOption(option);
    // window.addEventListener("resize", function() {
    //   myChart.resize();
    // });

})();
