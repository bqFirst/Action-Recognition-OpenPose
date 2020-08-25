

var data_view = {
    config: {
        table: layui.table,
        tableId: 'idTest',
        page: layui.laypage,
        curPage: 1,
        domId: 'table_demo4',
        tableId: 'laypage_1',
        pageLimit: $('.row-num select').val()
    },
    saveObj:{
        id:'',
        name:'',
        alias:'',
        dataLinkId:''
    },
    optArr:[],
    tableData: [
        // { "id": 10000, "field1": "广州", "field2": 100, "field3": 200, "field4": 300, "field5": "2018-01-01" },
        // { "id": 10001, "field1": "中山", "field2": 101, "field3": 201, "field4": 301, "field5": "2018-01-01" },
        // { "id": 10002, "field1": "深圳", "field2": 102, "field3": 202, "field4": 302, "field5": "2018-01-02" },
        // { "id": 10003, "field1": "佛山", "field2": 103, "field3": 203, "field4": 303, "field5": "2018-01-03" }
    ],
    tableCols: [
        // [
        //     { type: 'checkbox' },
        //     { field: 'field1', title: '<input type="checkbox" title="" lay-skin="primary"><i class="icon icon-sjy-abc"></i><span class="table-menu"></span>区域', sort: true, edit: 'text' },
        //     { field: 'field2', title: '<input type="checkbox" title="" lay-skin="primary"><i class="icon icon-sjy-123"></i><span class="table-menu"></span>总人口(万人)', sort: true, edit: 'text' },
        //     { field: 'field3', title: '<input type="checkbox" title="" lay-skin="primary"><i class="icon icon-sjy-123"></i><span class="table-menu"></span>男性人口(万人)', sort: true, edit: 'text' },
        //     { field: 'field4', title: '<input type="checkbox" title="" lay-skin="primary"><i class="icon icon-sjy-123"></i><span class="table-menu"></span>女性人口(万人)', sort: true, edit: 'text' },
        //     { field: 'field5', title: '<input type="checkbox" title="" lay-skin="primary"><i class="icon icon-sjy-rili"></i><span class="table-menu"></span>统计时间', sort: true, edit: 'text' },
        // ]
    ],
    initLayPage: function(total, cur,size){
    	
        var curr = cur ? cur : 1;
        var limit = size ? size : 10;
        var count = total ? total : 0;
        //var limits = [50,100,500];

        data_view.config.pageLimit = limit;
        data_view.config.curPage = curr;
        
        layui.laypage.render({
            elem: 'laypage_1'
            ,count: count
            ,curr: curr
            ,limit: limit
            //,limits:limits
            ,layout: ['count', 'prev', 'page', 'next', 'limit', 'skip']
            ,jump: function(obj,first){
            	
            	data_view.config.curPage = obj.curr;
                data_view.config.pageLimit = obj.limit;

                data_view.getSessionTempData().then(function(temp_data){
                	var x_tmpCols = data_view['tableOrgCol'];
                	var x_tmpCols_size = x_tmpCols == null ? 0 : x_tmpCols.length;
                    data_view.initData(x_tmpCols,temp_data,x_tmpCols_size);
                    data_view.initTable();
                });
                
            }
            
        });

        
    },
    jumpToLastPage: function() {
        data_view.getSessionData('tableData').then(function(dd){
            if(dd != null){
                var pageLimit = data_view.config.pageLimit ? data_view.config.pageLimit : 10;
                var arr = (dd.length / pageLimit).toString().split('.');
                var lastPage = 1;
                if(arr.length > 1){
                    lastPage = Number(arr[0]) + 1;
                }else{
                    lastPage = Number(arr[0]);
                }
    
            }
            data_view.config.curPage = lastPage;
    
            data_view.initLayPage(dd ? dd.length : 0, data_view.config.curPage, data_view.config.pageLimit);
    
    
            data_view.getSessionTempData().then(function(){
                data_view.initTable();
            });
            ;
        });
    },
    saveSessionData: function(key, data){
        /* if(key){
            layui.sessionData('data_view', {key: key, value: data});
        }else{
            layui.sessionData('data_view', null);
        } */
        if(key){
            return localforage.setItem(key,data);
        }else{
            return localforage.clear();
        }

    },
    getSessionData: function(key){
        return localforage.getItem(key);
    },
    addSessionData: function(data){
        return data_view.getSessionData('tableData').then(function(dd){
            dd.push(data);

            dd.forEach((e,i) => {//reset row index
                e['ROW_INDEX'] = i;
            });
        
            return data_view.saveSessionData('tableData',dd);

        });
        

    },
    addSessionDataCol: function(newCol){
        return data_view.getSessionData('tableData').then(function(dd){
            if(dd != null && dd.length > 0){
                dd.forEach(e => {
                    e[newCol.name] = null;
                });
            }
    
            return data_view.saveSessionData('tableData',dd);
        });
        
    },
    updateSessionData: function(data){
        return data_view.getSessionData('tableData').then(function(dd){
            var row_index = data['ROW_INDEX'];
            dd.splice(row_index,1,data);
            return data_view.saveSessionData('tableData',dd);
        });
        

    },
    deleteSessionData: function(data){
        return data_view.getSessionData('tableData').then(function(dd){
            data.forEach(d =>{
                var flag = false;
                var index = null;
                dd.filter(function(v,i) {
                    if(d['ROW_INDEX'] == v['ROW_INDEX']){
                        flag = true;
                        index = i;
                        return true;
                    }
                });
    
                if(flag){
                    dd.splice(index, 1);
                }
            });
            dataLength = dd.length;
            return data_view.saveSessionData('tableData',dd);
        });
        
    },
    deleteSessionCol: function(deleteCols){
        return data_view.getSessionData('tableData').then(dd => {
            if(dd != null && dd.length > 0){
                dd.forEach(e => {
                    deleteCols.forEach(deleteCol => {
                        if(e.hasOwnProperty(deleteCol)){
                            delete e[deleteCol];
                        }
                    });
                });
                return data_view.saveSessionData('tableData',dd);
            }
        });
    },
    getSessionTempData: function(){
        return data_view.getSessionData('tableData').then(function(temp_data){
            var conf = data_view.config;
            var cur = conf.curPage;
            var limit = conf.pageLimit;
            var result = null;
            if(temp_data != null && temp_data.length > 0){
                result = temp_data.slice((cur -1) * limit, cur * limit);
            }
            return result;
        });
       

    },
    tableChangedData: [],
    maxCol:0,
    tableOrgCol:[],
    colOperations:[],
    addOperate: function(colName,type){
        data_view.colOperations.push({"colName":colName,"type":type});
    },
    initData: function(tableOrgCol,tableData,maxCol) {
    	
        data_view.tableOrgCol = tableOrgCol ? tableOrgCol : data_view.tableOrgCol;
        if(data_view.tableOrgCol != null && data_view.tableOrgCol.length > 0){
            data_view.tableCols = data_view.handleCols(data_view.tableOrgCol);
            data_view.tableData = tableData ? tableData : data_view.tableData;
            data_view.maxCol = maxCol;
        }else{
            data_view.tableCols = [];
            data_view.tableData = [];
        }
        //this.tableCols = tableCols;
    },
    initParams: function(){
        if(this.config.table == null){
            this.config.table = layui.table;
        }

        if(this.config.laypage == null){
            this.config.laypage = layui.laypage;
        }

        this.config.pageLimit = $('.row-num select').val();
    },
    buildTableData: function(tableOrgCol,tableData){
        var temp_data = [];
        if(tableData != null && tableData.length > 0){
            tableData.forEach((e,i) => {
                var temp = {};
                tableOrgCol.forEach(f => {
                    temp[f['name']] = e[f['name']];
                });
                
                temp['ROW_INDEX'] = e['ROW_INDEX'];
                temp_data.push(temp);
            });
        }
        //console.log(temp_data);
        return temp_data;
    },
    initTable: function () { //初始化table
        if(this.config.table == null){
            this.config.table = layui.table;
        } 
        var table_data = data_view.buildTableData(this.tableOrgCol,this.tableData);
        var tableData = this.tableData;
        var elemId = this.config.domId;
        this.tableChangedData = table_data;
        
        //设置-表头的宽度.begin.
        if(this.tableCols != null && this.tableCols.length >0){
        	var tmpColList = this.tableCols[0];
        	if(tmpColList != null){
        		var defaultWidth = 130;//默认130宽度.
        		var defaultDateWith = 165;//时间类型的默认宽度.
        		for(var i in tmpColList){
                	var tmpCol = tmpColList[i];
                	if('checkbox' == tmpCol['type']){
                		continue;
                	}
                	var width = defaultWidth;
                	var originAlias = tmpCol['originAlias'];
                	if(originAlias != null){
                		var len = originAlias.length;
                		var tmpWidth = len * 26;
                		if(tmpWidth > width){
                			width = tmpWidth;
                		}
                	}
                	
                	//对时间类型强制设置宽度.
                	if( ("TimeStamp" == tmpCol['columnType'] || "Date" == tmpCol['columnType']) && width < defaultDateWith){
                		width = defaultDateWith;
                	}
                	
                	tmpCol['width'] = width;
                }
        	}
        }
        //设置-表头的宽度.end.
        
        this.config.table.render({
            elem: '#' + elemId,
            height: 'full-220',
            limit: this.config.pageLimit,
            text: {
                none: '暂无数据'
            },
            id: this.config.tableId,
            data: table_data,
            cols: this.tableCols,
            page: false
            ,cellMinWidth:130//设置表格的最小宽度.
        });

        // this.config.table.on('edit(idTest)', function(obj){
        //     console.log(obj);
        //    var value = obj.value //得到修改后的值
        //    ,data = obj.data //得到所在行所有键值
        //    ,field = obj.field; //得到字段
        // //    layer.msg( field + ' 字段更改为：'+ value);
        
        //  });
        this.unbindTh();

        //监听单元格编辑
        this.config.table.on('edit(table_edit)', function (obj) {
            //console.log(obj);
            var value = obj.value //得到修改后的值
                , data = obj.data //得到所在行所有键值
                , field = obj.field; //得到字段
            // layer.msg(field + ' 字段更改为：' + value);
            var dd = tableData[Number(data.LAY_TABLE_INDEX)];
            dd[field] = value;

            data_view.updateSessionData(dd);
            return;
        });

        lay('.datebox').each(function(a,b) {
            var temp = $(b);
            var column_type = temp.attr('column_type');
            var format_str = "yyyy-MM-dd";
            var type_str = 'date';
            if(column_type == 'Date'){
                format_str = "yyyy-MM-dd"
                type_str = 'date';
            }else if(column_type = 'TimeStamp'){
                format_str = 'yyyy-MM-dd HH:mm:ss'
                type_str = 'datetime';
            }
            laydate.render({
                elem: this,
                trigger: 'click',
                format :format_str,
                type:type_str,
                done: function(value, date,c){
                    var column_name = temp.attr('column_name');
                    var data_index = temp.attr('data_index');

                    var dd = tableData[Number(data_index)];
                    dd[column_name] = value;
                    data_view.updateSessionData(dd);
                }
            });
        });
        
    },
    insertRow: function () { //插入行

        var newRow = {};
        var orgCols = this.tableOrgCol;
        var tableData = this.tableData;
        if(orgCols != null && orgCols.length > 0 ){
            orgCols.forEach(e => { //Number,String,Date,TimeStamp, NULL,Long,Double, Bytes, Boolean,COIN;
                if(e['columnType'] == 'Date' || e['columnType'] == 'TimeStamp' ){
                    newRow[e['name']] = '';
                }else{
                    newRow[e['name']] = null;
                }
            });
        }
        data_view.addSessionData(newRow).then(function(){
            data_view.jumpToLastPage();
        });
        


        /* var newRow = {};
        var orgCols = this.tableOrgCol;
        var tableData = this.tableData;
        if(orgCols != null && orgCols.length > 0 ){
            orgCols.forEach(e => { //Number,String,Date,TimeStamp, NULL,Long,Double, Bytes, Boolean,COIN;
                if(e['columnType'] == 'Date' || e['columnType'] == 'TimeStamp' ){
                    newRow[e['name']] = '';
                }else{
                    newRow[e['name']] = null;
                }
            });
        }
        tableData.push(newRow);
        this.initTable();
        this.unbindTh();

        var hiddenThArr = [];
        $('#cus-table-demo4 .layui-table th').each(function () {
            if ($(this).hasClass('hidden')) {
                hiddenThArr.push($(this).attr('data-field'));
            }
        });
        for (var i = 0; i < hiddenThArr.length; i++) {
            $('#cus-table-demo4 .layui-table th[data-field="' + hiddenThArr[i] + '"]').addClass('hidden');
            $('#cus-table-demo4 .layui-table td[data-field="' + hiddenThArr[i] + '"]').addClass('hidden');
        } */
    },
    deleteRow: function () { //删除行
        
        //var tableChangedData = data_view.config.table.cache.idTest;
        var tableChangedData = data_view.config.table.cache.laypage_1; //改成分页
        var tableData = this.tableData;
        var newTableData = [];
        var checkedArr = [];
        if(tableChangedData != undefined && tableChangedData.length > 0){
            var hasChecked = false;
            tableChangedData.forEach((e,i) =>{
                if(!e['LAY_CHECKED']){
                    // newTableData.push(tableData[e['LAY_TABLE_INDEX']]);
                    //console.log(e);
                    tableData.forEach((f,j) =>{
                        if(f['ROW_INDEX'] == e['ROW_INDEX']){
                            newTableData.push(f);
                        }
                    });
                }else{
                    hasChecked = true;
                    checkedArr.push(e);
                }
            });

            if(!hasChecked){
                // opts.push("DELETE_ROW");
                pop_info("没有勾选删除行");
            }else{
                layer.confirm('确定要删除所选行？', {
                    title:"删除",
                    btn: ['取消', '确定'],
                    btn2: function(index, layero) {
                        // data_view.tableData = newTableData;
                        // data_view.initTable();
                        if(checkedArr != null && checkedArr.length > 0){
                            data_view.deleteSessionData(checkedArr).then(function(dd){
                                data_view.initLayPage(dd ? dd.length : 0,data_view.config.curPage,data_view.config.pageLimit);
                                data_view.getSessionTempData().then(function(temp_data){
                                    data_view.initData(null,temp_data,null);
                                    data_view.initTable();
                                });
                            });
                           
                        }
                    }
                });
            }
        }
    },
    insertCol: function () { //插入列
        var orgCols = this.tableOrgCol;
        var tableData = this.tableData;
        $('.pop-cont-tableColInsert input').val('');
        $('.pop-cont-tableColInsert').removeClass('hide');
        var addOperate = this.addOperate;
        layer.open({
            type: 1,
            skin: 'layer-over form-box1',
            title: '列名',
            area: ['300px', 'auto'], //宽高
            content: $('.pop-cont-tableColInsert'),
            btn: ['取消', '确定'],
            btn2: function(index1, layero1) {
                //layer.msg($('.pop-cont-tableColInsert input').val(), { icon: 9 });
                // var column_name = "col_" + (orgCols ? orgCols.length + 1 : 1);
                var column_name = "col_" + (new Date()).getTime();
                var temp_alias = $('.pop-cont-tableColInsert input').val();

                if(temp_alias != null){
                    if(temp_alias.length > 0 && temp_alias.length <= 30){
                        if(!data_view.validateRepeat(orgCols,null,temp_alias)){
                            var newCol = {"alias": temp_alias,"name":column_name,"columnType":"String"}
                            orgCols.push(newCol);
                            if(tableData != null && tableData.length > 0){
                                tableData.forEach(e => {
                                    e[column_name] = null;
                                });
                            }

                            addOperate(column_name,"INSERT");

                            data_view.addSessionDataCol(newCol).then(function(){
                                data_view.initData(orgCols,tableData);
                                data_view.initTable();
                            });
                        }else{
                            pop_info("列名重复,请重新命名");
                            return false;//不关闭弹窗
                        }
                    }else if(temp_alias.length <= 0){
                        pop_info("名称不能为空");
                    }else if(temp_alias.length > 30){
                        pop_info("名称不能超过30个字符");
                    }
                }

                

            },
            end: function(index1, layero1) {
                $('.pop-cont-tableColInsert').addClass('hide');
            }
        });
    },
    deleteCol: function () { //删除列
        var tableData = this.tableData;
        var tableOrgCol = this.tableOrgCol;
        var addOperate = this.addOperate;
        var hasChecked = false;

        $('#cus-table-demo4 .layui-table th').each(function() {
            if ($(this).find('.layui-form-checked').length > 0) {
                hasChecked = true;
            }
        });

        if(hasChecked){
            layer.confirm('确定要删除选择列？', {
                title:"删除",
                btn: ['取消', '确定'],
                btn2: function(index, layero) {
                    var deleteCols = [];
                    var newOrgCols = [];
                    $('#cus-table-demo4 .layui-table th').each(function() {
                        if ($(this).find('.layui-form-checked').length > 0) {
                            //console.log($(this).attr('data-field'));
                            var deleteCol = $(this).attr('data-field');
                            if(tableData != null && tableData.length > 0){
                                tableData.forEach(e => {
                                    if(e.hasOwnProperty(deleteCol)){
                                        delete e[deleteCol];
                                    }
                                    if(e.hasOwnProperty('LAY_TABLE_INDEX')){
                                        delete e['LAY_TABLE_INDEX']
                                    }    
                                });
                            }
                            
                            deleteCols.push(deleteCol);
                            addOperate(deleteCol,"DELETE");
                            hasChecked = true;
                        }
                    });



                    if(tableOrgCol != null && tableOrgCol.length > 0){
                        newOrgCols = tableOrgCol.filter(e => {
                            var flag = true;
                            deleteCols.forEach( deleteCol =>{
                                if(e['name'] == deleteCol){
                                    flag = false;
                                }
                            });
                            return flag;
                        });

                    }

                    if(deleteCols != null && deleteCols.length > 0){
                        data_view.deleteSessionCol(deleteCols).then(function(){
                            tableOrgCol = newOrgCols;
                            data_view.initData(tableOrgCol,tableData);
                            data_view.initTable();
                        });
                    }
                }
            });
            
        }else{
            pop_info("没有勾选删除列");
        }

    },
    findCol: function(col){
        var orgCols = this.tableOrgCol;
        var tempCol = null
        if(orgCols != null && orgCols.length > 0){
            orgCols.forEach(e => {
                if(e['name'] == col){
                    tempCol = e;
                }
            });
        }
        return tempCol;
    },
    parseDataType: function(col,data){
        //console.log(col);
        var column_name = col['name'];
        var column_type = col['columnType'];

        if(data != null && data.length > 0){
            data.forEach(e => {
                e[column_name] = data_view.parseDataByType(e[column_name],column_type);
            });
        }
    },
    parseDataByType: function (data, column_type) {
        var result = null;
        if(data != null){
            if(column_type == "Long"){
                var temp = Number(data);
                if(!isNaN(temp)){
                    result = temp.toFixed();
                }
            }else if(column_type == "Double"){
                var temp = Number(data);
                if(!isNaN(temp)){
                    result = temp;
                }
            }else if(column_type == "String"){
                result = String(data);
            }else if(column_type == "Date"){
                if (data) { 
                    var temp_date = new Date(data.replace(/-/,"/"));
                    if(temp_date != "Invalid Date"){
                        //result = temp_date;
                        result = temp_date.Format("yyyy-MM-dd");
                    }
                }
            }else if(column_type == "TimeStamp"){
                if (data) { 
                    var arr1 = data.split(" "); 
                    var sdate = arr1[0].split('-'); 
                    var temp_date = new Date(sdate[0], sdate[1]-1, sdate[2]); 
                    if(temp_date != "Invalid Date"){
                        // result = temp_date;
                        result = temp_date.Format("yyyy-MM-dd hh:mm:ss");
                    }
                } 
            }
        }
        return result;
    },
    getSelectContent: function(type){
        var option_str = "";
        if(type == "Long"){
            option_str += '<option value="String">字符串</option><option value="Double">小数</option>';
        }else if(type == "Double"){
            option_str += '<option value="String">字符串</option><option value="Long">整数</option>';
        }else if(type == "Date"){
            option_str += '<option value="String">字符串</option>';
        }else if(type =="TimeStamp"){
            option_str += '<option value="String">字符串</option>';
        }else if(type =="String"){
            option_str += '<option value="Long">整数</option><option value="Double">小数</option><option value="Date">日期</option><option value="TimeStamp">时间戳</option>';
        }
        return option_str;
    },
    changeColType: function (col) { //修改列类型
        var tempCol = this.findCol(col);
        var addOperate = this.addOperate;
        var tableOrgCol = this.tableOrgCol;
        var tableData = this.tableData;
        var oldType = tempCol['columnType'];

        var option_str = data_view.getSelectContent(oldType);
        
        $('.pop-cont-tableColType select option').remove();
        $('.pop-cont-tableColType select').append(option_str);
        layui.form.render('select');

        $('.pop-cont-tableColType').removeClass('hide');
        layer.open({
            type: 1,
            skin: 'layer-over form-box1',
            title: '修改数据类型',
            area: ['300px', 'auto'], //宽高
            content: $('.pop-cont-tableColType'),
            btn: ['取消', '确定'],
            btn2: function(index1, layero1) {
                // layer.msg($('.pop-cont-tableColType').find('input').val(), { icon: 9 });
                var newType = $('.pop-cont-tableColType').find('select').val();
                tempCol['columnType'] = newType;

                addOperate(tempCol['name'],"CHANGETYPE");

                data_view.getSessionData('tableData').then(function(dd){
                    data_view.parseDataType(tempCol,dd);
                    
                    data_view.getSessionTempData().then(function(temp_data){
                        data_view.initData(tableOrgCol,temp_data);
                        data_view.initTable();
                    });
                });

                
            },
            end: function(index1, layero1) {
                $('.pop-cont-tableColType').addClass('hide');
            }
        });

    },
    validateRepeat: function(data,col,newAlias){
        var flag = false;
        if(data != null && data.length > 0){
            for(var i = 0; i < data.length ; i++){
                var temp_data = data[i];
                if(temp_data['alias'] == newAlias){
                    if(col != null && col == temp_data['name']){ //修改列名且与原来名称相同
                        flag = false; // 不算重复
                    }else{
                        flag = true;//重复
                    }
                }
            }
        }

        return flag;
    },
    renameCol: function (col) { //重命名列
        $('.pop-cont-tableColRename').removeClass('hide');
        $('.pop-cont-tableColRename').find('input').val('');
        var tableOrgCol = this.tableOrgCol;
        var tableData = this.tableData;
        var addOperate  = this.addOperate;
        var tempCol = this.findCol(col);
        $('.pop-cont-tableColRename').find('input').val(tempCol['alias']);
        layer.open({
            type: 1,
            skin: 'layer-over form-box1',
            title: '重命名',
            area: ['300px', 'auto'], //宽高
            content: $('.pop-cont-tableColRename'),
            btn: ['取消', '确定'],
            btn2: function(index1, layero1) {
                // layer.msg($('.pop-cont-tableColRename').find('input').val(), { icon: 9 });
                var newAlias = $('.pop-cont-tableColRename').find('input').val();
                if(newAlias != null){
                    if(newAlias.length <= 30){
                        if(!data_view.validateRepeat(tableOrgCol,col,newAlias)){//判断是否重复
                            tableOrgCol.forEach(function(e) {
                                if(e['name'] == col){
                                    e['alias'] = newAlias;
                                    addOperate(col,"RENAME");
                                }
                            });
                            data_view.initData(tableOrgCol,tableData);
                            data_view.initTable();
                        }else{
                            pop_info("列名重复,请重新命名");
                            return false;//不关闭弹窗
                        }
                    }else{
                        pop_info("名称不能超过30个字符");
                    }
                }
                
            },
            end: function(index1, layero1) {
                $('.pop-cont-tableColRename').addClass('hide');
            }
        });
    },
    saveDataAs: function(){
        // data_view.saveObj.data = this.tableData;
        data_view.getSessionData('tableData').then(function(dd){
            data_view.saveObj.data = dd;
            data_view.saveObj.tableCol = data_view.tableOrgCol;   
            data_view.saveObj.tableCol.forEach(e => {
                delete e.table;
            });
            var temp_saveObj = data_view.saveObj;
            $('.pop-cont-saveAs').removeClass('hide');
            $('.pop-cont-saveAs').find('input').val('');
            layer.open({
                type: 1,
                skin: 'layer-over form-box1',
                title: '另存为名称',
                area: ['300px', 'auto'], //宽高
                content: $('.pop-cont-saveAs'),
                btn: ['取消', '确定'],
                btn2: function(index1, layero1) {
                    // layer.msg($('.pop-cont-tableColType').find('input').val(), { icon: 9 });
                    var temp_name = $('.pop-cont-saveAs').find('input').val();
                    if(temp_name != null && temp_name.length > 0){
                        temp_saveObj.alias = temp_name;
                        var saveObj = JSON.stringify(temp_saveObj);
                        var url = getCTX() + "/dataEdit/saveAs.do";
                        //console.log(saveObj);

                        $.ajax({
                            url : url,
                            data : saveObj,
                            dataType: "json",  
                            contentType:'application/json',
                            traditional: true,
                            type : "POST",
                            success : function(json){
                                if(json.msg == 'success'){
                                    pop_succeed("保存成功");
                                }else{
                                    pop_failure("保存失败");
                                }
                            },
                            
                            error: function(XMLHttpRequest, textStatus, errorThrown) {
                                pop_failure("保存失败");
                            },				
                        });
                    }else{
                        pop_info("输入名称为空,无法保存");
                    }
                },
                end: function(index1, layero1) {
                    $('.pop-cont-saveAs').addClass('hide');
                }
            });
        });

    },
    saveData: function() {
        //data_view.saveObj.data = this.tableData;
        data_view.getSessionData('tableData').then(function(dd){
            data_view.saveObj.data = dd;
            data_view.saveObj.tableCol = data_view.tableOrgCol;
            data_view.saveObj.colOperations = data_view.colOperations;
            data_view.saveObj.tableCol.forEach(e => {
                delete e.table;
            });
            var saveObj = JSON.stringify(data_view.saveObj);
            var url = getCTX() + "/dataEdit/save.do";
            //console.log(saveObj);
            $.ajax({
                url : url,
                data : saveObj,
                dataType: "json",  
                contentType:'application/json',
                traditional: true,
                type : "POST",
                success : function(json){
                    if(json.status == 'OK'){
                        pop_succeed(json.msg);
                        data_view.colOperations = [];
                    }else{
                        pop_failure(json.msg);
                    }		    	
                },
                
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    pop_failure("保存失败");
                },				
            });
        });

    },
    handleCols: function(cols) {
        var tableCols = [];
        var tempCols = [];
        if (cols != null && cols.length > 0) {
            //tableCols.push({field: 'ROW_INDEX', hide:false ,title:'row_index'});
            cols.forEach(e => {
            	//拷贝一个名称.
            	var originAlias = e['alias'];
                var col_type = e['columnType'];
                var editEnable = true;
                var col_icon = 'abc';
                if(col_type == 'Long'||col_type == 'Double'){
                    col_icon = '123';
                }else if(col_type == 'Date'||col_type == 'TimeStamp'){
                    col_icon = 'rili'
                    editEnable = false;
                }else{ //默认字符

                }
                var iconStr =  '<i class="icon icon-sjy-'+ col_icon + '" ></i>';
                var menuStr =  '';
                var nameStr = '<span>'+e['alias']+'</span>';
                var sourceAlias = e['sourceAlias'];
                if(sourceAlias == null || "null" == sourceAlias){
                	sourceAlias = "";
                }
                if("" != sourceAlias && sourceAlias != e['alias']){
                	nameStr = '<span class="help-iconbtn2" tips-txt="原字段名:'+sourceAlias+'" >'+e['alias']+'</span>';
                }
                var tmpTitle = iconStr +menuStr +nameStr ;
                var temp_field = { field: e['name'], title:tmpTitle, sort: true, originAlias:originAlias,columnType:e['columnType'] };
                if(!editEnable){
                    delete temp_field.edit;
                }

                tableCols.push(temp_field);
            });
            tempCols.push(tableCols);
        }
        return tempCols;
    },
    unbindTh: function() {
        $('.cus-table th').unbind('click');
    },
    changeLimit: function(val){
        var temp_config = this.config;
        var tableData = this.tableData;
        var dataLength = tableData ? tableData.length : 0;
        if(val != undefined){
            if(val == ''){
                temp_config.pageLimit = dataLength;        
            }else{
                temp_config.pageLimit = Number(val);
            }
        }
        this.initTable();
    }

};

//监听单元格编辑
// var layTable = layui.table
// layTable.on('edit(idTest)', function(obj){
//     console.log(obj);
//    var value = obj.value //得到修改后的值
//    ,data = obj.data //得到所在行所有键值
//    ,field = obj.field; //得到字段
//    layer.msg('[ID: '+ data.id +'] ' + field + ' 字段更改为：'+ value);

//  });
function loadData(dataLinkId,id) {
	console.log('加载数据dataLinkId['+dataLinkId+'],id['+id+']'+new Date().getTime());
	
	var loadingDialogIdx = layer.msg('正在加载数据...', {
		icon : 11,
		shade : true,
		time : 0
	});
	
    var url = getCTX() + "/dataEdit/viewTableData.do";
    data_view.saveSessionData();//数据设置为空
    $.post(url,{'id':id},function(e){
    	
    	//数据加载完成.关闭加载对话框.
    	layer.close(loadingDialogIdx);
    	
        var tableData = e.returnData.tableData; 
        var columns = tableData.columns;
        var dataList = tableData.dataList;
        
        var maxCol = columns.length;
        var tableId = tableData.id;
        var tableName = tableData.name;
        var tableAlias = tableData.alias;

        data_view.saveObj.id = tableId;
        data_view.saveObj.name = tableName;
        data_view.saveObj.alias = tableName;
        data_view.saveObj.dataLinkId = dataLinkId;

        if(columns != null && columns.length > 0){
            
            if(dataList != null && dataList.length > 0){
                dataList.forEach((e,i) => {
                    e['ROW_INDEX'] = i;
                });
            }
            
            
            //赋值.到 属性.
            data_view['tableOrgCol'] = columns;
            data_view['tableData'] = dataList;
            
            
            data_view.saveSessionData('tableData', dataList).then(function(e){
                
            	data_view.initLayPage(dataList.length);
            	
            	/**/
                data_view.getSessionTempData().then(function(temp_data){
                    data_view.initData(columns,temp_data,maxCol);
                    data_view.initTable();
                });
                
                
            }).catch(function(error) {
            	// 处理 getJSON 和 前一个回调函数运行时发生的错误
            	console.log('发生错误！', error);
            });

            

        }else{
            layer.msg("数据表为空",{icon:9});
        }

        $('#tableName').text(tableAlias);

        
        
    });


// 对Date的扩展，将 Date 转化为指定格式的String 
// 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符， 
// 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字) 
// 例子： 
// (new Date()).Format("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423 
// (new Date()).Format("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18 
Date.prototype.Format = function(fmt) 
{ //author: meizz 
  var o = { 
    "M+" : this.getMonth()+1,                 //月份 
    "d+" : this.getDate(),                    //日 
    "h+" : this.getHours(),                   //小时 
    "m+" : this.getMinutes(),                 //分 
    "s+" : this.getSeconds(),                 //秒 
    "q+" : Math.floor((this.getMonth()+3)/3), //季度 
    "S"  : this.getMilliseconds()             //毫秒 
  }; 
  if(/(y+)/.test(fmt)) 
    fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length)); 
  for(var k in o) 
    if(new RegExp("("+ k +")").test(fmt)) 
  fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length))); 
  return fmt; 
} 


var active = {
    getCheckData: function () { //获取选中数据
        var checkStatus = table.checkStatus('idTest')
            , data = checkStatus.data;
        pop_info(JSON.stringify(data));
    }, 
    getCheckLength: function () { //获取选中数目
        var checkStatus = table.checkStatus('idTest')
            , data = checkStatus.data;
        pop_info('选中了：' + data.length + ' 个');
    }, 
    isAll: function () { //验证是否全选
        var checkStatus = table.checkStatus('idTest');
        pop_info(checkStatus.isAll ? '全选' : '未全选');
    }
};

function getData() {
    var data = [
        { "id": 10000, "field1": "广州", "field2": 100, "field3": 200, "field4": 300, "field5": "2018-01-01" },
        { "id": 10001, "field1": "中山", "field2": 101, "field3": 201, "field4": 301, "field5": "2018-01-01" },
        { "id": 10002, "field1": "深圳", "field2": 102, "field3": 202, "field4": 302, "field5": "2018-01-02" },
        { "id": 10003, "field1": "佛山", "field2": 103, "field3": 203, "field4": 303, "field5": "2018-01-03" }
    ];

    var cols = [
        { name: 'name1', field: 'field1' },
        { name: 'name2', field: 'field2' },
        { name: 'name3', field: 'field3' },
        { name: 'name4', field: 'field4' },
        { name: 'name5', field: 'field5' }
    ];


    data_view.tableData = data;
    data_view.tableCols = handleCols(cols);
}



function removeCol(field) {
    if(cols != null && cols.length > 0){
        var arr = cols.filter(e => {
            return e['field'] == field;
        });
    }
}



function handleCols(cols) {
    var tableCols = [];
    if (cols != null && cols.length > 0) {
        tableCols.push({ type: 'checkbox' });
        cols.forEach(e => {
            tableCols.push({ field: e['name'], title: '<input type="checkbox" title="" lay-skin="primary"><i class="icon icon-sjy-abc"></i><span class="table-menu"></span>' + e['alias'], sort: true, edit: 'text' });
        });
        return [tableCols];
    }else{
        return [];
    }
}


$(document).on('click','#data_view_save',function(e){
    data_view.saveData();
});

$(document).on('click','#data_view_saveAs',function(e){
    data_view.saveDataAs();
});

// $(document).on('change','.row-num select',function(e){
//     console.log(this);
//     console.log(e);
// });


$("#row_num_select").change(function(e){  
    //console.log(this);
    //console.log(e); 
})   
}



