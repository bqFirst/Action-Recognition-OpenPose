var niceScroll_option = {
    cursorcolor: '#999',
    cursorwidth: '8px',
    cursorborder: '0',
    cursorborderradius: '4px',
    background: 'rgba(0,0,0,0)'
};

function scrollInit() {
    $('.scroll').niceScroll(niceScroll_option);
}

layui.define(['layer', 'element', 'table'], function(exports) {

    var $ = layui.jquery,
        layer = layui.layer,
        element = layui.element,
        table = layui.table;

    $(document).on('click', '#pop_succeed', function() {
        layer.msg('成功', { icon: 7 });
    });

    $(document).on('click', '#pop_failure', function() {
        layer.msg('失败', { icon: 8 });
    });

    $(document).on('click', '#pop_info', function() {
        layer.msg('信息', { icon: 9 });
    });

    $(document).on('click', '#pop_network', function() {
        layer.msg('网络不稳定，请稍后再尝试', { icon: 10 });
    });

    $(document).on('click', '#pop_running', function() {
        layer.msg('缩略图正在保存', { icon: 11, shade: true, time: 0 });
    });

    $(document).on('click', '#pop_1', function() {
        layer.confirm('确定要删除项目？', {
            btn: ['取消', '确定'],
            btn2: function(index, layero) {
                layer.msg('点击了确定', { icon: 9 });
            }
        });
    });

    function tableScroll() {
        $('.layui-table-main').niceScroll(niceScroll_option);
    }

    function tableInit(tableid) {
        table.render({
            elem: tableid,
            url: 'data/table1.json',
            initSort: { field: 'ziduan', type: 'asc' },
            cellMinWidth: 50,
            text: {
                none: '无样本数据，请单击 [ 运行 ] 生成样本'
            },
            cols: [
                [
                    { type: 'numbers' },
                    { field: 'ziduan', title: '字段字段字段字段字段字段字段字段字段字段字段', sort: true },
                    { field: 'pingjunzhi', title: '平均值', width: 100 },
                    { field: 'yunxingjieguo', title: '运行结果', width: 100, templet: '#runResultsTpl' }
                ]
            ],
            page: false
        });
        tableScroll();
    }

    $(document).on('click', '#pop_2', function() {
        $('.pro-cont-viewData').removeClass('hide');
        tableInit('#table1');
        layer.open({
            type: 1,
            title: '查看数据',
            skin: 'layer-over viewData',
            area: ['800px', '500px'], //宽高
            content: $('.pro-cont-viewData'),
            btn: ['取消', '确定'],
            btn2: function(index, layero) {

            },
            end: function(index, layero) {
                $('.pro-cont-viewData').addClass('hide');
            }
        });
    });

    $(document).on('click', '#pop_3', function() {
        $('.pro-cont-viewLog').removeClass('hide');
        layer.open({
            type: 1,
            title: '查看日志',
            skin: 'layer-over viewLog',
            area: ['800px', 'auto'], //宽高
            content: $('.pro-cont-viewLog'),
            btn: ['取消', '确定'],
            btn2: function(index, layero) {

            },
            end: function(index, layero) {
                $('.pro-cont-viewLog').addClass('hide');
            }
        });
        scrollInit();
    });

    $(document).on('click', '#pop_4', function() {
        $('.pro-cont-samplePop').removeClass('hide');
        //tableInit('#table2');

        table.init('parse-table-demo', { //转化静态表格
            height: 'full-340'
        });

        layer.open({
            type: 1,
            title: '样本1',
            skin: 'layer-over samplePop',
            area: ['800px', '580px'], //宽高
            content: $('.pro-cont-samplePop'),
            btn: ['取消', '确定'],
            btn2: function(index, layero) {

            },
            end: function(index, layero) {
                $('.pro-cont-samplePop').addClass('hide');
            }
        });
    });

    //tab
    var wrapWidth;
    var tabStep = 120 * 3;

    function tabsMul() {
        wrapWidth = $('.tabbox').width();
        autoJudge();
    }

    var widthFn = function(element) { //获取宽度
        var sum_width = 0;
        element.children('li').each(function() {
            sum_width += parseInt($(this).width()) + 15;
        });
        return sum_width;
    }

    //自判断tab
    function autoJudge() {
        var tabUl = widthFn($('.tabbox').find('.layui-tab-title'));
        if (wrapWidth >= tabUl) {
            $('.tabbox').removeClass('more');
        } else {
            $('.tabbox').addClass('more');
        }
    }

    $(window).resize(autoJudge);

    var stepFn = function(element, my_origin, wrapWidth, topnav_width, flag) { //获取步距
        var step_width = 0;

        if (flag) {
            var b = my_origin;
            if (b < 0) {
                var a = tabStep + my_origin;
                return parseInt(a);
            }
        } else {
            var b = topnav_width - my_origin;
            if (b > wrapWidth) {
                var a = tabStep - my_origin;
                return parseInt(a);
            }
        }
        return step_width;
    }

    $(document).on('click', '.tabbox .tab-iconleft', function() {
        var element = $(this).siblings('.layui-tab-title');
        var topnav_width = widthFn(element);
        if (topnav_width <= wrapWidth) return false;
        var my_origin = element.css('marginLeft');
        var nav_step = stepFn(element, parseInt(my_origin), wrapWidth, topnav_width, true);
        var my_total = parseInt(nav_step) + 0;
        if (parseInt(my_total) % tabStep != 0) {
            return false;
        }
        element.css('margin-left', my_total);
    });

    $(document).on('click', '.tabbox .tab-iconright', function() {
        var element = $(this).siblings('.layui-tab-title');
        var topnav_width = widthFn(element);
        if (topnav_width <= wrapWidth) return false;
        var my_origin = element.css('marginLeft');
        var nav_step = stepFn(element, parseInt(my_origin), wrapWidth, topnav_width, false);
        var my_total = 0 - parseInt(nav_step) + 0;
        if (parseInt(my_total) % tabStep != 0) {
            return false;
        }
        if (topnav_width - Math.abs(parseInt(my_origin)) <= wrapWidth) return false; //已无隐藏无需滚动
        element.css('margin-left', my_total);
    });

    //tab删除
    element.on('tabDelete(consoleTab)', function(data) {
        autoJudge();
    });

    $(document).on('click', '#pop_5', function() {
        $('.pro-cont-modelDetails').removeClass('hide');
        layer.open({
            type: 1,
            title: '模型详情',
            skin: 'layer-over modelDetails',
            area: ['800px', '580px'], //宽高
            content: $('.pro-cont-modelDetails'),
            btn: ['取消', '确定'],
            btn2: function(index, layero) {

            },
            end: function(index, layero) {
                $('.pro-cont-modelDetails').addClass('hide');
            }
        });
        scrollInit();
    });

    //tab切换
    element.on('tab(modelDetailsTab)', function(data) {
        if (data.index === 1) {
            tableInit('#table3');
            tabsMul();
        }
    });

    exports('pop', {});
});
