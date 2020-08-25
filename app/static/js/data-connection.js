layui.define(['element', 'layer', 'form', 'table','laydate','laypage'], function(exports) {

    var $ = layui.jquery,
        element = layui.element,
        layer = layui.layer,
        form = layui.form,
        table = layui.table;
        laydate = layui.laydate;

    //search-box2
    $('.search-box2 .search-input').bind('input propertychange', function() {
        var val = $(this).val();
        if (val == '') {
            $(this).parents('.search-box2').removeClass('active');
        } else {
            $(this).parents('.search-box2').addClass('active');
        }
    });
    $(document).on('click', '.search-box2 .search-del', function() {
        $(this).siblings('.search-input').val('');
        $(this).parents('.search-box2').removeClass('active');
    });
    $(document).on('click', '.search-box2 .search-submit', function() {
        //console.log($(this).siblings('.search-input').val());
    });
    $(document).on('keyup', '.search-box2 .search-input', function(e) {
        if (e.keyCode == 13) {
            //console.log($(this).val());
        }
    });

//    if($('input[name="id"]').val() == null || $('input[name="id"]').val().trim().length == 0){
//        $(document).on('keyup', 'input[name="name"]', function(e) {
//            $(".title .tit").text($(this).val());
//        });
//    }

    $(document).on('keyup', 'input[name="name"]', function(e) {
        var value = $(this).val().trim();
        $(".main-r-t .title .tit").text(value);
    });
    
    //tab
    $(document).on('click', '.cus-tab .cus-tab-head li', function() {
        if ($(this).hasClass('disabled')) {
            return false;
        }
        var _this = $(this),
            fa = _this.parents('.cus-tab'),
            flag = _this.attr('cus-tab-data');

        _this.addClass('active').siblings('li').removeClass('active');
        fa.find('.cus-tab-cont[cus-tab-data="' + flag + '"]').addClass('active').siblings('.cus-tab-cont').removeClass('active');
        $('.cus-tab-cont').getNiceScroll().resize();
    });

    //表格tab
    var wrapWidth;
    var tabStep = 160 * 3;

    function tabsMul() {
        wrapWidth = $('.tabbox').width();
        autoJudge();
    }

    var widthFn = function(element) { //获取宽度
        var sum_width = 0;
        element.children('li').each(function() {
            sum_width += parseInt($(this).width()) + 37;
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

    //tab删除前
    $(document).on('click', '.layui-tab .tab-close', function(e) {
        e.stopPropagation();
        var _this = $(this);
        
        var tabCount = $(".layui-tab .tab-close").length;
        if(tabCount <= 1){
        	pop_info('不能删除、至少保留一个数据表Tab.', { icon: 8 });
        }else{
            layer.confirm('是否删除此选项卡？', {
                title: "删除",
                btn: ['取消', '确定'],
                btn1: function () {
                    layer.closeAll();
                },
                btn2: function () {
                    _this.siblings('.layui-tab-close').click();
                }
            });
        }
        
        
    });

    //tab删除
    element.on('tabDelete(selectTab)', function(data) {
        autoJudge();
    });

    //tab切换
    element.on('tab(selectTab)', function(data) {
        scrollInit();
    });

    tabsMul();

    //重命名tab
    $(document).on('dblclick', '.tabbox .layui-tab-title li', function() {
        $(this).find('.tab-name').addClass('active');
        $(this).find('.tab-name .inp').select();
    });
    $(document).on('blur', '.tabbox .layui-tab-title li .tab-name.active .inp', function() {
        var val = $.trim($(this).val());
        $(this).siblings('.name').text(val).attr('title', val);
        $(this).parents('.tab-name').removeClass('active');
        if (val == '') {
            pop_info("名称不可以为空");
            return false;
        }
    });
    //回车事件
    var defaultTableName = "数据表-X";
    $(document).on('keyup', '.tabbox .layui-tab-title li .tab-name.active .inp', function(e) {
    	var val = $.trim($(this).val());
    	if(val == null || ''== val){
    		$(this).val(defaultTableName);
    		pop_info('名称不可以为空-当前设置为默认值('+defaultTableName+')');
    	}
        if (e.keyCode == 13) {
            $(this).blur();
        }
    });

    //表头选择
    $(document).on('click', '.table-type1 tr', function() {
        var index = $(this).find('.table-head i').text();

        if ($(this).hasClass('active')) {
            $(this).removeClass('active');
            $(this).prevAll('tr').removeClass('disabled');
            $(this).parents('table').find('thead tr').removeClass('disabled');
            $('#table-index').text(0);
        } else {
            $(this).parents('table').find('tr').removeClass('active disabled');
            $(this).addClass('active');
            $(this).prevAll('tr').addClass('disabled');
            if (index > 1) {
                $(this).parents('table').find('thead tr').addClass('disabled');
            }
            $('#table-index').text(index);
        }
    });

    //切换tab的时候行数变化
    element.on('tab(selectTab)', function(data) {
        var index = $(data.elem).find('.layui-tab-content .layui-tab-item').eq(data.index).find('tr.active .table-head i').text();
        $('#table-index').text(index);
    });

    //基本信息保存按钮
    $(document).on('click', '#tab-dataconn1-save', function() {
        parent.layer.msg('保存成功', { icon: 7 });
        $('#tab-dataconn .cus-tab-head li.disabled').removeClass('disabled');
    });

    //表格高度
    $('.table-type1-demo').css({
        'max-height': $(window).height() - 320
    });

    //头部tab
    $(document).on('click', '#tab-dataconn .cus-tab-head li', function() {
        if ($(this).hasClass('disabled')) {
        	parent.layer.msg('请先保存数据连接', { icon: 9 });
            return ;
        }
        var index = $(this).index();
        if(File_Preview_Ins == null){
        	File_Preview_Ins = {};//防止空指针.
        }
        
        if (index == 0) {
            tabsMul();
            //表格高度
            $('.table-type1-demo').css({
                'max-height': $(window).height() - 320
            });
        } else if (index == 1) {
        	//加载 数据连接的表格.
        	File_Preview_Ins.loadDataLinkTableList();
        	
            //初始化table
            //table.init('table-demo1', {
            //    height: 'full-180',
            //    text: {
            //        none: '暂无数据'
            //    }
            //});
            
        } else if (index == 2) {
            //初始化table
        	//加载 数据连接的 主题列表.
        	File_Preview_Ins.loadDataLinkThemeList();
            
            //table.init('table-demo2', {
            //    height: 'full-130',
            //    text: {
            //       none: '暂无数据'
            //    }
            // });
            
        }
    });

    //初始化table
    table.init('table-demo3', {
        height: 'full-80',
        text: {
            none: '暂无数据'
        }
    });

    //cus-table
    unbindTh();

    function unbindTh() {
        $('.cus-table th').unbind('click');
    }

    //显示隐藏列
    $(document).on('click', '#coldisplay_btn', function() {
        var fa = $(this).parents('.table-box');
        if ($(this).find('.layui-form-checkbox').hasClass('layui-form-checked')) {
            fa.find('.cus-table').removeClass('hidden-row');
        } else {
            fa.find('.cus-table').addClass('hidden-row');
        }
    });

    //table-box工具栏
    ////插入行
    var addColIndex = 10003;
    $(document).on('click', '.table-tool-addRow', function() {

        data_edit.insertRow();
        /* var oldData = table.cache['table_demo4'];
        var data1 = { "id": addColIndex + 1, "field1": "珠海", "field2": 104, "field3": 204, "field4": 304, "field5": "2018-01-04" };
        oldData.push(data1);
        var hiddenThArr = [];
        $('#cus-table-demo4 .layui-table th').each(function() {
            if ($(this).hasClass('hidden')) {
                hiddenThArr.push($(this).attr('data-field'));
            }
        });
        table.reload('table_demo4', {
            data: oldData
        });
        unbindTh();
        for (var i = 0; i < hiddenThArr.length; i++) {
            $('#cus-table-demo4 .layui-table th[data-field="' + hiddenThArr[i] + '"]').addClass('hidden');
            $('#cus-table-demo4 .layui-table td[data-field="' + hiddenThArr[i] + '"]').addClass('hidden');
        } */

    });
    ////插入列
    $(document).on('click', '.table-tool-addCol', function() {
        //parent.tableAddCol();
        data_edit.insertCol();
    });
    ////删除行
    $(document).on('click', '.table-tool-delRow', function() {
        // parent.tableDelRow();
        var checkStatus = table.checkStatus('table_demo4');
        data_edit.deleteRow();
    });
    ////删除列
    $(document).on('click', '.table-tool-delCol', function() {
        //parent.tableDelCol();
        /* $('#cus-table-demo4 .layui-table th').each(function() {
            if ($(this).find('.layui-form-checked').length > 0) {
                console.log($(this).attr('data-field'));
            }
        }); */
        data_edit.deleteCol();
    });

    //table-menu
    var selcol;
    $(document).on('click', '.table-menu', function(e) {
        e.stopPropagation();
        selcol = e.target.offsetParent.offsetParent;
        if ($(selcol).hasClass('hidden')) {
            $('#table_menu_coldisplay').addClass('active').text('取消隐藏');
        } else {
            $('#table_menu_coldisplay').removeClass('active').text('设为隐藏');
        }
        var menu_w = 100;
        var left = $(e.target).offset().left,
            top = $(e.target).offset().top + 30;
        if (menu_w + $(e.target).offset().left > $(window).width()) {
            left = left - menu_w + 20;
        }
        $('.popout-tableMenu').addClass('active').css({
            'left': left,
            'top': top
        });
    });

    //设为隐藏列
    $(document).on('click', '#table_menu_coldisplay', function() {
        var col = $(selcol).attr('data-field');
        if ($(this).hasClass('active')) {
            $('th[data-field="' + col + '"],td[data-field="' + col + '"]').removeClass('hidden');
        } else {
            $('th[data-field="' + col + '"],td[data-field="' + col + '"]').addClass('hidden');
        }
    });

    //修改数据类型
    $(document).on('click', '#pop-tableColType', function(e) {
        var col = $(selcol).attr('data-field');
        // parent.tableColType(col);
        data_edit.changeColType(col);
    });

    //列重命名
    $(document).on('click', '#pop-tableColRename', function(e) {
        var col = $(selcol).attr('data-field');
        // parent.tableColRename(col);
        data_edit.renameCol(col);
    });
    
    //保存连接
    form.on('submit(saveConn)', function(data){ 
    	var url = ctx + "/DBDataLink/saveConn";
    	var classifyId = $("#classifySelect").find("option:selected").val();
    	if (!classifyId) {
            parent.layer.msg('请选择分类', { icon: 9 });
    		return false;
    	}
    	data.field.classify = {};
    	data.field.classify.id = classifyId;
    	var classifyName = $('#classifySelect').find("option:selected").text();
    	var mask = parent.layer.msg('测试连接中...', {icon:9,shade: [0.5],scrollbar: false, time:35000}) ;
        $.ajax({
            url: url,
            type: 'POST',
            data: JSON.stringify(data.field),
            dataType :'json',
            contentType : 'application/json',
            success : function (result) {
            	parent.layer.close(mask);
            	 var msg = result.msg;
            	if(result.status == 'OK'){
                     parent.layer.msg(msg, { icon: 7 });
            		 var dataLinkId = result.returnData.id;
            		//改为直接跳转到树-内容页面
            		window.parent.location =ctx+ "/DataLink/Main.do?dataLinkId="+dataLinkId;
            	}else if(result.status == 'ERROR'){
            		msg = msg + "；数据连接保存失败";
                    parent.layer.msg(msg, { icon: 8 });
            	}
            },
            error : function(){
            	parent.layer.close(mask);
                parent.layer.msg("保存失败！", { icon: 8 });
            }
            
        });
    	return false;
    });
    
    //测试连接
    form.on('submit(testConn)', function(data){
    	var url = ctx + "/DBDataLink/testConn"
    	var mask = parent.layer.msg('测试连接中...', {icon:9,shade: [0.5],scrollbar: false, time:35000}) ;
        $.ajax({
            url: url,
            type: 'POST',
            data: JSON.stringify(data.field),
            dataType :'json',
            contentType : 'application/json',
            success : function (result) {
            	parent.layer.close(mask);
				if(result.status=='OK'){
					$('#testResult').val(result.msg);
                    parent.layer.msg(result.msg, { icon: 7 });
				}else{
                    parent.layer.msg('连接测试失败,'+result.msg+',请填写正确的信息再测试', { icon: 8 });
				}
            },
            error : function(){
            	parent.layer.close(mask);
                parent.layer.msg("服务器错误！", { icon: 8 });
            }
        })
        return false;
    });
    
  //创建数据主题
    $("#createDataTheme").on('click',function(){
    	var param = $("input[name='id']").val();
    	parent.window.location.href = ctx + "/DataTheme/addMain.do?dataLinkId=" + param;
    });

    form.verify({
    	maxlength: function(value, item) {
            var str = $.trim(value);
            if(str.length > 100){
            	return '名称长度不能超过100个字符';
            }
        }
    });

    //头部tab
    $(document).on('click', '#tab-databaseconn .cus-tab-head li', function() {
        var index = $(this).index();
        if (index == 0) {

        } else if (index == 1) {
            //初始化table
            table.init('table-demo5', {
                height: 'full-185',
                text: {
                    none: '暂无原始表'
                }
            });
        } else if (index == 2) {
            //初始化table
            table.init('table-demo2', {
                height: 'full-130',
                text: {
                    none: '暂无数据'
                }
            });
        }
    });

    //头部tab
    $(document).on('click', '#tab-databaseconn-biaoxinxi .cus-tab-head li', function() {
        var index = $(this).index();
        if (index == 0) {
            //初始化table
            table.init('table-demo5', {
                height: 'full-185',
                text: {
                    none: '暂无原始表'
                }
            });
        } else if (index == 1) {
            //初始化table
            table.init('table-demo6', {
                height: 'full-185',
                text: {
                    none: '暂无自定义SQL视图'
                }
            });
        }
    });

    //查看数据
    $(document).on('click','.viewData-btn',function(){
    	var dataLinkId = $("input[name='id']").val();
    	
    	var columnUrl = null;
    	var dataUrl = null;
    	var where = {};
    	var name = '';
    	if($(this).hasClass("oprationView")){
    		var viewId = $(this).attr('value');
    		if(viewId.length > 0){
                columnUrl = ctx + "/DataLink/column/view/" + viewId;
                dataUrl = ctx + "/DataLink/data/view/" + viewId;
                name = $(this).attr('name');
    		}

    	}else if($(this).hasClass("oprationTable")){
    		var tableName = $(this).attr('value');
    		if(tableName.length > 0){
                columnUrl = ctx + "/DataLink/column/table.do";
                dataUrl = ctx + "/DataLink/data/table.do";
                where = {tableName : tableName, dataLinkId: dataLinkId};
                name = tableName;
    		}
    	}

    	parent.DataLinkMain_Ins.viewData(columnUrl, dataUrl, where,name);
    });
    
    $(document).on('click','.datathemehref',function(){
		var viewId = $(this).attr('value');
		$("input[name='targetThemeId']").val(viewId);
		$("#datathemeform").submit();
    });
    
    form.on('select(row_num_select)', function(e){
        var temp_val = e['value'];
        data_edit.changeLimit(temp_val);
    });


    $("#cancel").on('click',function(){
    	parent.window.location.href = ctx + "/DataLink/Main.do";
    });
    
    exports('data-connection', {});

});
