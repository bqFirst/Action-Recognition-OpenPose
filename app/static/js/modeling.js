layui.define(['element', 'layer', 'form', 'table'], function(exports) {

    var $ = layui.jquery,
        element = layui.element,
        layer = layui.layer,
        form = layui.form,
        table = layui.table;

    //监听单选操作
    form.on('radio(radioDemo)', function(obj) {
        console.log(this.value + ' ' + this.name + '：' + obj.elem.checked, obj.othis);
    });

    //监听过滤器操作
    form.on('switch(switchDemo)', function(obj) {
        console.log(this.value + ' ' + this.name + '：' + obj.elem.checked, obj.othis);
    });

    //监听处理操作
    form.on('select(selectDemo)', function(data) {
        console.log(data);
        var sel_id = data.othis[0].previousElementSibling.id;
        if (data.value == 3) {
            var val;
            $('.pro-cont-designatedValue').removeClass('hide');
            layer.open({
                type: 1,
                title: '指定值填补',
                skin: 'layer-over designatedValue',
                area: ['400px', 'auto'], //宽高
                content: $('.pro-cont-designatedValue'),
                btn: ['取消', '确定'],
                btn2: function(index1, layero1) {
                    val = $('.designatedValue input[name="designatedValue-radio"]:checked').val();
                    if (val === '常量') {
                        var str = $.trim($('.designatedValue .changliang').val());
                        if (str == '') {
                            layer.msg('请输入常量', { icon: 8 });
                            return false;
                        } else {
                            val = '常量值：' + str;
                        }
                    }
                    $('#' + sel_id).siblings('.layui-form-select').find('.layui-select-title .layui-input').val(val);
                },
                end: function(index1, layero1) {
                    $('.pro-cont-designatedValue').addClass('hide');
                }
            });
        }
    });

    //tab
    var wrapWidth;
    var tabStep = 140 * 3;

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
        //var my_total = 0 - parseInt(nav_step) + 0;
        //element.css('margin-left', my_total > 0 ? 0 : my_total);
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

    //tab删除前
    $(document).on('click', '.layui-tab .tab-close', function() {
        var _this = $(this);
        layer.confirm('是否删除此选项卡？', {
            btn: ['取消', '确定'],
            btn1: function() {
                layer.closeAll();
            },
            btn2: function() {
                _this.siblings('.layui-tab-close').click();
            }
        });
        e.stopPropagation();
    });

    //tab删除
    element.on('tabDelete(consoleTab)', function(data) {
        autoJudge();
    });

    //tab切换
    element.on('tab(consoleTab)', function(data) {
        scrollInit();
    });

    function tableScroll() {
        $('.layui-table-main').niceScroll(niceScroll_option);
    }

    function modelingCont(index) {
        if (index == 1) {
            /*table.render({
                elem: '#table1',
                url: 'data/table1.json',
                initSort: { field: 'ziduan', type: 'asc' },
                cellMinWidth: 50,
                height: 'full-214',
                text: {
                    none: '无样本数据，请单击 [ 运行 ] 生成样本'
                },
                cols: [
                    [
                        { type: 'numbers' },
                        { field: 'xuanzhe', title: '', width: 50, templet: '#radioTpl' },
                        { field: 'ziduan', title: '字段', width: 100, sort: true },
                        { field: 'pingjunzhi', title: '平均值', width: 100, sort: true },
                        { field: 'guolvqi', title: '过滤器', width: 80, templet: '#switchTpl' },
                        { field: 'bieming', title: '别名', width: 180, templet: '#textTpl' },
                        { field: 'caozuo', title: '操作', width: 100, templet: '#operateTpl' },
                        { field: 'chuli', title: '处理', width: 180, templet: '#selectTpl' }
                    ]
                ],
                page: false
            });
            tableScroll();*/
            table.init('parse-table-demo');
        }
        if (index == 2) {
            table.render({
                elem: '#table2',
                url: 'data/table1.json',
                initSort: { field: 'ziduan', type: 'asc' },
                cellMinWidth: 50,
                text: {
                    none: '无样本数据，请单击 [ 运行 ] 生成样本'
                },
                cols: [
                    [
                        { type: 'numbers' },
                        { field: 'xuanzhe', title: '', width: 50, templet: '#radioTpl' },
                        { field: 'ziduan', title: '字段', width: 100, sort: true },
                        { field: 'pingjunzhi', title: '平均值', width: 100, sort: true },
                        { field: 'guolvqi', title: '过滤器', width: 80, templet: '#switchTpl' },
                        { field: 'bieming', title: '别名', width: 180, templet: '#textTpl' },
                        { field: 'caozuo', title: '操作', width: 100, templet: '#operateTpl' },
                        { field: 'chuli', title: '处理', width: 180, templet: '#selectTpl' }
                    ]
                ],
                page: false
            });
            tableScroll();
        }
        if (index == 3) {
            table.render({
                elem: '#table3',
                url: 'data/table1.json',
                initSort: { field: 'ziduan', type: 'asc' },
                cellMinWidth: 50,
                height: 'full-214',
                text: {
                    none: '无样本数据，请单击 [ 运行 ] 生成样本'
                },
                cols: [
                    [
                        { type: 'numbers' },
                        { field: 'xuanzhe', title: '', width: 50, templet: '#radioTpl' },
                        { field: 'ziduan', title: '字段', width: 100, sort: true },
                        { field: 'pingjunzhi', title: '平均值', width: 100, sort: true },
                        { field: 'guolvqi', title: '过滤器', width: 80, templet: '#switchTpl' },
                        { field: 'bieming', title: '别名', width: 180, templet: '#textTpl' },
                        { field: 'caozuo', title: '操作', width: 100, templet: '#operateTpl' },
                        { field: 'chuli', title: '处理', width: 180, templet: '#selectTpl' }
                    ]
                ],
                page: false
            });
            tableScroll();
        }
        if (index == 5) {
            table.render({
                elem: '#table5',
                url: 'data/table1.json',
                initSort: { field: 'ziduan', type: 'asc' },
                cellMinWidth: 50,
                height: 'full-214',
                text: {
                    none: '无样本数据，请单击 [ 运行 ] 生成样本'
                },
                cols: [
                    [
                        { type: 'numbers' },
                        { field: 'xuanzhe', title: '', width: 50, templet: '#radioTpl' },
                        { field: 'ziduan', title: '字段', width: 100, sort: true },
                        { field: 'pingjunzhi', title: '平均值', width: 100, sort: true },
                        { field: 'guolvqi', title: '过滤器', width: 80, templet: '#switchTpl' },
                        { field: 'bieming', title: '别名', width: 180, templet: '#textTpl' },
                        { field: 'caozuo', title: '操作', width: 100, templet: '#operateTpl' },
                        { field: 'chuli', title: '处理', width: 180, templet: '#selectTpl' }
                    ]
                ],
                page: false
            });
            tableScroll();
        }
        if (index == 6) {
            table.render({
                elem: '#table6',
                url: 'data/table1.json',
                initSort: { field: 'ziduan', type: 'asc' },
                cellMinWidth: 50,
                text: {
                    none: '无样本数据，请单击 [ 运行 ] 生成样本'
                },
                cols: [
                    [
                        { type: 'numbers', fixed: 'left' }, //固定列
                        { field: 'xuanzhe', title: '', width: 50, templet: '#radioTpl' },
                        { field: 'ziduan', title: '字段', width: 200, sort: true },
                        { field: 'pingjunzhi', title: '平均值', width: 200, sort: true },
                        { field: 'guolvqi', title: '过滤器', width: 80, templet: '#switchTpl' },
                        { field: 'bieming', title: '别名', width: 180, templet: '#textTpl' },
                        { field: 'caozuo', title: '操作', width: 100, templet: '#operateTpl' },
                        { field: 'chuli', title: '处理', width: 180, templet: '#selectTpl' }
                    ]
                ],
                page: false
            });
            tableScroll();
        }
        if (index == 7) {
            table.render({
                elem: '#table7',
                url: 'data/table1.json',
                initSort: { field: 'ziduan', type: 'asc' },
                cellMinWidth: 50,
                height: 'full-262',
                text: {
                    none: '无样本数据，请单击 [ 运行 ] 生成样本'
                },
                cols: [
                    [
                        { type: 'numbers' },
                        { field: 'ziduan', title: '字段', width: 100, sort: true },
                        { field: 'pingjunzhi', title: '平均值', width: 100, sort: true }
                    ]
                ],
                page: false
            });
            tableScroll();
        }
        if (index == 8) {
            table.render({
                elem: '#table8',
                url: 'data/table1.json',
                initSort: { field: 'ziduan', type: 'asc' },
                cellMinWidth: 50,
                text: {
                    none: '无样本数据，请单击 [ 运行 ] 生成样本'
                },
                cols: [
                    [
                        { type: 'numbers' },
                        { field: 'ziduan', title: '字段', width: 100, sort: true },
                        { field: 'pingjunzhi', title: '平均值', width: 100, sort: true }
                    ]
                ],
                page: false
            });
            tableScroll();
        }
        if (index == 9) {
            table.render({
                elem: '#table9',
                url: 'data/table1.json',
                initSort: { field: 'ziduan', type: 'asc' },
                cellMinWidth: 50,
                height: 'full-260',
                text: {
                    none: '无样本数据，请单击 [ 运行 ] 生成样本'
                },
                cols: [
                    [
                        { type: 'numbers' },
                        { field: 'ziduan', title: '字段', width: 100, sort: true },
                        { field: 'tuxing', title: '图形', width: 120, sort: true, templet: '#chartTpl' },
                        { field: 'pingjunzhi', title: '平均值', width: 100, sort: true }
                    ]
                ],
                page: false
            });
            tableScroll();
        }
        if (index == 10) {
            table.render({
                elem: '#table10',
                url: 'data/table1.json',
                initSort: { field: 'ziduan', type: 'asc' },
                cellMinWidth: 50,
                text: {
                    none: '无样本数据，请单击 [ 运行 ] 生成样本'
                },
                cols: [
                    [
                        { type: 'numbers' },
                        { field: 'ziduan', title: '字段', width: 100, sort: true },
                        { field: 'pingjunzhi', title: '平均值', width: 100, sort: true }
                    ]
                ],
                page: false
            });
            $('.sel-model').selection();
            tableScroll();
            tabsMul();
        }
    }

    //初始化table和滚动条
    modelingCont(1);
    $('.modeling-cont1').niceScroll(niceScroll_option);

    //删除loading
    setTimeout(function() {
        $('.loading-shade').remove();
    }, 1000);

    //建模过程右击菜单
    var process_right_click;
    $('.modeling-process').bind('contextmenu', function() {
        return false;
    });
    $('.modeling-process .item .num,.modeling-process .item .text').mousedown(function(e) {
        var fa = $(this).parents('.item');

        if (e.which == 1) {
            var index = fa.index() + 1;
            fa.addClass('active').siblings('.item').removeClass('active');
            $('.modeling-cont' + index).addClass('active').siblings('.modeling-cont').removeClass('active');
            modelingCont(index);
            $('.modeling-cont' + index).niceScroll(niceScroll_option);
        }

        if (e.which == 3 && !fa.hasClass('loading')) {
            process_right_click = fa.index();

            if (fa.hasClass('skip')) {
                $('.popout-process li .process-run-btn').addClass('disabled');
                $('.popout-process li .process-skip-btn').addClass('active').html('<i class="icon icon-sjjm-tiaoguo"></i>恢复此处');
            } else {
                $('.popout-process li .process-run-btn').removeClass('disabled');
                $('.popout-process li .process-skip-btn').removeClass('active').html('<i class="icon icon-sjjm-tiaoguo"></i>跳过');
            }
            if (process_right_click == 0 || process_right_click == 5 || process_right_click == 8) {
                $('.process-run-btn').parents('li').addClass('hide');
                $('.process-skip-btn').parents('li').addClass('hide');
            } else if (process_right_click == 9) {
                $('.process-run-btn').parents('li').removeClass('hide');
                $('.process-skip-btn').parents('li').addClass('hide');
            } else {
                $('.process-run-btn').parents('li').removeClass('hide');
                $('.process-skip-btn').parents('li').removeClass('hide');
            }

            var left = e.pageX + 15,
                top;
            if ($(window).height() - e.pageY < 150) {
                top = e.pageY - $('.popout-process').height();
            } else {
                top = e.pageY + 15;
            }
            $('.popout-process').addClass('active').css({
                'left': left,
                'top': top
            });
        }

    });

    //放大图片
    $(document).on('click', '.chratImg-zoomIn', function(e) {
        layer.open({
            type: 1,
            skin: 'layer-img',
            title: false, //不显示标题
            area: ['800px', 'auto'], //宽高
            content: $(this).html()
        });
    });

    //离散化-字段方式
    form.on('radio(discretize_zdfs)', function(data) {
        if (data.value == '覆盖原始字段') {
            $(data.elem).parents('.layui-form-item').siblings('.layui-form-item3').addClass('hide');
        } else {
            $(data.elem).parents('.layui-form-item').siblings('.layui-form-item3').removeClass('hide');
        }
    });

    //离散化-离散化方法
    form.on('select(discretize_lshff)', function(data) {
        $(data.elem).parents('.panel-head').siblings('.panel-body').children('.lshff-cont').eq(data.value).addClass('active').siblings('.lshff-cont').removeClass('active');
    });

    //离散化-删除
    $(document).on('click', '.discretize-box .item-close', function() {
        $(this).parents('.item').remove();
    });

    //离散化-添加
    $(document).on('click', '.discretize-box .item-add', function() {
        var html = '<div class="item">' +
            '    <div class="layui-form">' +
            '        <div class="layui-form-item layui-form-item1">' +
            '            <div class="layui-inline">' +
            '                <label class="layui-form-label">离散化字段：</label>' +
            '                <div class="layui-input-inline">' +
            '                    <div class="sel-model" style="width: 400px">' +
            '                        <div class="model-del help-iconbtn" tips-txt="清空"></div>' +
            '                        <div class="model-txt">' +
            '                            <div class="model-txtbox"></div>' +
            '                        </div>' +
            '                        <span class="model-icon icon-sjjm-xiajiantou"></span>' +
            '                        <ul class="model-list">' +
            '                            <li name="all"><a>全选</a></li>' +
            '                            <li name="advise"><a>advise</a></li>' +
            '                            <li name="sales"><a>sales</a></li>' +
            '                            <li name="num"><a>num</a></li>' +
            '                            <li name="num1"><a>num1</a></li>' +
            '                            <li name="num2"><a>num2</a></li>' +
            '                            <li name="num3"><a>num3</a></li>' +
            '                            <li name="num4"><a>num2</a></li>' +
            '                            <li name="num5"><a>num3</a></li>' +
            '                        </ul>' +
            '                    </div>' +
            '                </div>' +
            '            </div>' +
            '        </div>' +
            '        <div class="layui-form-item layui-form-item2">' +
            '            <div class="layui-inline">' +
            '                <label class="layui-form-label">字段方式：</label>' +
            '                <div class="layui-input-inline">' +
            '                    <input type="radio" name="zdfs" value="新增字段" title="新增字段" checked lay-filter="discretize_zdfs">' +
            '                    <input type="radio" name="zdfs" value="覆盖原始字段" title="覆盖原始字段" lay-filter="discretize_zdfs">' +
            '                </div>' +
            '            </div>' +
            '        </div>' +
            '        <div class="layui-form-item layui-form-item3">' +
            '            <div class="layui-inline">' +
            '                <label class="layui-form-label">扩展名：</label>' +
            '                <div class="layui-input-inline">' +
            '                    <input type="text" class="layui-input">' +
            '                    <div class="tips">新增字段</div>' +
            '                </div>' +
            '            </div>' +
            '            <div class="layui-inline">' +
            '                <label class="layui-form-label">添加为：</label>' +
            '                <div class="layui-input-inline">' +
            '                    <input type="radio" name="tjw" value="后缀" title="后缀" checked>' +
            '                    <input type="radio" name="tjw" value="前缀" title="前缀">' +
            '                </div>' +
            '            </div>' +
            '        </div>' +
            '        <div class="cus-panel margin-top40">' +
            '            <div class="panel-head">' +
            '                <div class="layui-inline">' +
            '                    <label class="layui-form-label">离散化方法</label>' +
            '                    <div class="layui-input-inline">' +
            '                        <select lay-filter="discretize_lshff">' +
            '                            <option value="0">等距离散化</option>' +
            '                            <option value="1">分位数离散化</option>' +
            '                            <option value="2">均值-标准差离散化</option>' +
            '                        </select>' +
            '                    </div>' +
            '                </div>' +
            '            </div>' +
            '            <div class="panel-body">' +
            '                <div class="lshff-cont lshff-cont1 active">' +
            '                    <div class="layui-form-item layui-form-item1 margin-bottom30">' +
            '                        <div class="layui-inline">' +
            '                            <div class="layui-input-inline">' +
            '                                <input type="radio" name="djlsh" value="距离宽度" title="距离宽度" checked>' +
            '                                <div class="layui-input-inline">' +
            '                                    <input type="text" class="layui-input">' +
            '                                    <div class="tips">浮点数（最大3位小数）</div>' +
            '                                </div>' +
            '                            </div>' +
            '                        </div>' +
            '                    </div>' +
            '                    <div class="layui-form-item layui-form-item2 margin-bottom30">' +
            '                        <div class="layui-inline">' +
            '                            <div class="layui-input-inline">' +
            '                                <input type="radio" name="djlsh" value="离散数" title="离散数">' +
            '                                <div class="layui-input-inline">' +
            '                                    <input type="text" class="layui-input">' +
            '                                    <div class="tips">正整数</div>' +
            '                                </div>' +
            '                            </div>' +
            '                        </div>' +
            '                    </div>' +
            '                </div>' +
            '                <div class="lshff-cont lshff-cont2">' +
            '                    <div class="layui-form-item layui-form-item1">' +
            '                        <div class="layui-inline">' +
            '                            <div class="layui-input-inline">' +
            '                                <input type="radio" name="fwslsh" value="四分位数" title="四分位数" checked>' +
            '                                <input type="radio" name="fwslsh" value="五分位数" title="五分位数">' +
            '                                <input type="radio" name="fwslsh" value="十分位数" title="十分位数">' +
            '                                <input type="radio" name="fwslsh" value="二十分位数" title="二十分位数">' +
            '                                <input type="radio" name="fwslsh" value="百分位数" title="百分位数">' +
            '                            </div>' +
            '                        </div>' +
            '                    </div>' +
            '                    <div class="layui-form-item layui-form-item2">' +
            '                        <div class="layui-inline">' +
            '                            <div class="layui-input-inline">' +
            '                                <input type="radio" name="fwslsh" value="自定义" title="自定义">' +
            '                                <input type="text" class="layui-input">' +
            '                                <div class="text">分位数</div>' +
            '                            </div>' +
            '                        </div>' +
            '                    </div>' +
            '                </div>' +
            '                <div class="lshff-cont lshff-cont3">' +
            '                    <div class="layui-form-item layui-form-item1">' +
            '                        <div class="layui-inline">' +
            '                            <div class="layui-input-inline">' +
            '                                <input type="radio" name="jzbzclsh" value="0" title="+/- 1 标准差" checked>' +
            '                                <input type="radio" name="jzbzclsh" value="1" title="+/- 2 标准差">' +
            '                                <input type="radio" name="jzbzclsh" value="2" title="+/- 3 标准差">' +
            '                            </div>' +
            '                        </div>' +
            '                    </div>' +
            '                </div>' +
            '            </div>' +
            '        </div>' +
            '    </div>' +
            '</div>';
        $(this).before(html);
        form.render();
        $('.sel-model').selection();
    });

    //流程-保存
    $(document).on('click', '.modeling-process-head .btn-group .save-btn', function() {
        var _this = $(this),
            fa = _this.parents('.modeling-cont'),
            index = fa.attr('modeling_index'),
            item = $('.modeling-process').find('.item').eq(index - 1);

        item.addClass('save');
    });

    //流程-跳过
    $(document).on('click', '.modeling-process-head .btn-group .skip-btn', function() {
        var _this = $(this),
            fa = _this.parents('.modeling-cont'),
            index = fa.attr('modeling_index'),
            next = parseInt(index) + 1,
            item = $('.modeling-process').find('.item').eq(index - 1);

        if (_this.hasClass('active')) {
            _this.removeClass('active').html('跳过');
            _this.siblings('.run-btn').removeClass('layui-btn-disabled').addClass('layui-btn-normal');
            item.removeClass('skip');
        } else {
            _this.addClass('active').html('恢复此处');
            _this.siblings('.run-btn').removeClass('layui-btn-normal').addClass('layui-btn-disabled');
            item.addClass('skip').removeClass('active');

            $('.modeling-process').find('.item').eq(index).addClass('active');
            $('.modeling-cont' + index).removeClass('active');
            $('.modeling-cont' + next).addClass('active');
            modelingCont(next);
            $('.modeling-cont' + next).niceScroll(niceScroll_option);
        }
    });

    //流程-运行
    //流程-右击菜单-运行
    $(document).on('click', '.modeling-process-head .btn-group .run-btn,.process-run-btn', function() {
        var _this = $(this);

        if (_this.hasClass('layui-btn-disabled') || _this.hasClass('disabled')) {
            return false;
        }

        if (_this.hasClass('process-run-btn')) {
            index = parseInt(process_right_click) + 1;
        } else {
            index = _this.parents('.modeling-cont').attr('modeling_index');
            _this.addClass('active');
        }

        $('.modeling-process').find('.item').removeClass('succeed failure log');

        var d_a = 0;
        var new_a = 0;
        for (var i = 0; i < index; i++) {
            var d_a_pre = 0;
            (function(a) {
                var flag = $('.modeling-process').find('.item').eq(a).hasClass('skip');
                if (flag) {
                    d_a++;
                    return false;
                }
                new_a = a - d_a;
                setTimeout(function() {
                    if (a !== 0) {
                        $('.modeling-process').find('.item').eq(d_a_pre).removeClass('loading').addClass('succeed log');
                    }
                    $('.modeling-process').find('.item').eq(a).addClass('loading');
                    d_a_pre = a;
                }, new_a * 2000);
            })(i);
        }
        setTimeout(function() {
            $('.modeling-process').find('.item').eq(index - 1).removeClass('loading').addClass('succeed log');
            //删除loading状态
            _this.removeClass('active');
        }, (new_a + 1) * 2000);
    });

    //流程-右击菜单-跳过
    $(document).on('click', '.process-skip-btn', function() {
        var _this = $(this),
            index = parseInt(process_right_click) + 1,
            next = parseInt(index) + 1,
            item = $('.modeling-process').find('.item').eq(process_right_click),
            btn = $('.modeling-cont' + index).find('.modeling-process-head .btn-group .skip-btn');

        if (_this.hasClass('active')) {
            _this.removeClass('active').html('<i class="icon icon-sjjm-tiaoguo"></i>跳过');
            item.removeClass('skip');
            btn.removeClass('active').html('跳过');
            btn.siblings('.run-btn').removeClass('layui-btn-disabled').addClass('layui-btn-normal');
        } else {
            _this.removeClass('active').html('<i class="icon icon-sjjm-tiaoguo"></i>恢复此处');
            item.addClass('skip').removeClass('active');
            btn.addClass('active').html('恢复此处');
            btn.siblings('.run-btn').removeClass('layui-btn-normal').addClass('layui-btn-disabled');

            var flag = $('.modeling-cont' + index).hasClass('active');
            if (flag) {
                $('.modeling-process').find('.item').eq(index).addClass('active');
                $('.modeling-cont' + index).removeClass('active');
                $('.modeling-cont' + next).addClass('active');
                modelingCont(next);
                $('.modeling-cont' + next).niceScroll(niceScroll_option);
            }
        }
    });

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
                    { field: 'ziduan', title: '字段', width: 100, sort: true },
                    { field: 'pingjunzhi', title: '平均值', width: 100 },
                    { field: 'yunxingjieguo', title: '运行结果', width: 100, templet: '#runResultsTpl' }
                ]
            ],
            page: false
        });
        tableScroll();
    }

    //流程-右击菜单-查看数据
    $(document).on('click', '.process-viewData-btn', function() {
        $('.pro-cont-viewData').removeClass('hide');
        tableInit('#table11');
        layer.open({
            type: 1,
            title: '查看数据',
            skin: 'layer-over viewData',
            area: ['800px', '500px'], //宽高
            content: $('.pro-cont-viewData'),
            btn: ['取消', '确定'],
            end: function(index, layero) {
                $('.pro-cont-viewData').addClass('hide');
            }
        });
    });

    //流程-右击菜单-查看日志
    $(document).on('click', '.process-viewLog-btn', function() {
        $('.pro-cont-viewLog').removeClass('hide');
        layer.open({
            type: 1,
            title: '查看日志',
            skin: 'layer-over viewLog',
            area: ['800px', 'auto'], //宽高
            content: $('.pro-cont-viewLog'),
            btn: ['取消', '确定'],
            end: function(index, layero) {
                $('.pro-cont-viewLog').addClass('hide');
            }
        });
        scrollInit();
    });

    //help-iconbtn
    var help_tips;
    $(document).on('mouseenter', '.help-iconbtn', function() {
        var _this = $(this);
        var txt = _this.attr('tips-txt');
        help_tips = layer.tips(txt, _this, {
            tips: 3,
            skin: 'tipsStyle',
            area: ['auto', 'auto']
        });
    });
    $(document).on('mouseleave', '.help-iconbtn', function() {
        layer.close(help_tips);
    });

    //table里的select判断
    $(document).on('click', '.layui-table-view .layui-form-select,.chart-tool .layui-form-select', function(e) {
        var a = $(e.currentTarget).offset().top;
        var b = $(window).height();
        if (b - a >= 170) {
            $(e.currentTarget).find('dl').removeClass('style2');
        } else {
            $(e.currentTarget).find('dl').addClass('style2');
        }
    });

    exports('modeling', {});

});
