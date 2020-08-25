function resizeFun() {
  //main-l-b-tree
  $('.main-l-b-tree .layui-colla-content').css({
    'height': $(window).height() - 60 - 104 - $('.main-l-b-tree .layui-colla-item').length * (30 + 2) + 'px'
  });
}
var ctx = '127.0.0.1:5000';
resizeFun();
$(window).resize(function() {
  resizeFun();
});
window.onload = function() {
  resizeFun();
  $(window).resize(function() {
    resizeFun();
  });
}

layui.define(['element', 'layer', 'form', 'table', 'laydate'], function(exports) {

  var $ = layui.jquery,
    element = layui.element,
    layer = layui.layer,
    form = layui.form,
    laydate = layui.laydate,
    table = layui.table;

  
  //main-l头部加号
  $(document).on('click', '.popout-mainLeftTitle-btn', function(e) {
    e.stopPropagation();
    if (e.which == 1) {
      if ($(e.target).parents('.main-r-cont').length > 0) {
        $('.cus-select', parent.document).removeClass('cus-selected');
        $('.popout-btn', parent.document).removeClass('active');
        $('.popout-box', parent.document).removeClass('active');
      }
      $('.cus-select').removeClass('cus-selected');
      $('.popout-btn').removeClass('active');
      $('.popout-box').removeClass('active');
    }
    mainLeftTitle = e.target.parentNode.id;
    $('.popout-mainLeftTitle-btn').removeClass('active');
    $(this).addClass('active');
    var left = e.pageX + 5,
      top;
    if ($(window).height() - e.pageY < 100) {
      top = e.pageY - $('.popout-mainLeftTitle').height();
    } else {
      top = e.pageY + 10;
    }
    $('.popout-mainLeftTitle').addClass('active').css({
      'left': left,
      'top': top
    });
    return false;
  });

  
  //main-l菜单
  $(document).on('click', '.popout-mainLeftTree-btn', function(e) {
    e.stopPropagation();
    if (e.which == 1) {
      if ($(e.target).parents('.main-r-cont').length > 0) {
        $('.cus-select', parent.document).removeClass('cus-selected');
        $('.popout-btn', parent.document).removeClass('active');
        $('.popout-box', parent.document).removeClass('active');
      }
      $('.cus-select').removeClass('cus-selected');
      $('.popout-btn').removeClass('active');
      $('.popout-box').removeClass('active');
      $('.popout-mainLeftTitle-btn').removeClass('active');
      $('.popout-mainLeftTitle').removeClass('active');
    }
    mainLeftTree = e.target.parentNode.id;
    var zTree = $.fn.zTree.getZTreeObj('main_left_tree');
    var treeNode = zTree.getNodeByTId(mainLeftTree);
    if (treeNode.isParent) {
      $('.popout-mainLeftTree').find('.dir-menu').removeClass('hide');
      $('.popout-mainLeftTree').find('.node-menu').addClass('hide');
    } else {
      $('.popout-mainLeftTree').find('.dir-menu').addClass('hide');
      $('.popout-mainLeftTree').find('.node-menu').removeClass('hide');
    }
    $('.popout-mainLeftTree-btn').removeClass('active');
    $(this).addClass('active');
    var left = e.pageX + 5,
      top;
    if ($(window).height() - e.pageY < 100) {
      top = e.pageY - $('.popout-mainLeftTree').height();
    } else {
      top = e.pageY + 10;
    }
    $('.popout-mainLeftTree').addClass('active').css({
      'left': left,
      'top': top
    });
    return false;
  });

  //main-l ztree
  function beforeExpand(treeId, treeNode) {
    if (treeNode.level == 0) {
      $.fn.zTree.getZTreeObj(treeId).expandAll(false);
    }
  }

  function beforeClick(treeId, treeNode, clickFlag) {
    return (treeNode.click != false);
  }

  function getCurrentRoot(treeNode) {
    if (treeNode.getParentNode() != null) {
      var parentNode = treeNode.getParentNode();
      return getCurrentRoot(parentNode);
    } else {
      return treeNode;
    }
  }

  function onExpand(e, treeId, treeNode) {
    var zTree = $.fn.zTree.getZTreeObj(treeId);
    if (treeNode.getParentNode()) {
      var nodes = treeNode.getParentNode().children;
      var nodesMe = treeNode;
    } else {
      var nodes = zTree.getNodes();
      var nodesMe = getCurrentRoot(treeNode);
    }
    for (var i = 0; i < nodes.length; i++) {
      if (nodes[i].tId != nodesMe.tId) {
        zTree.expandNode(nodes[i], false, true, false);
      }
    }
    if (treeId == 'pro_manage_tree') {
      $('.main-l-b-tree').getNiceScroll().resize();
    }
  }
  
  function onClick(e, treeId, treeNode) {
	  if (treeNode.isParent) {
		  var id = treeNode.dataId;
          $('.addDataConnection').attr("id",id);
          console.log($('.addDataConnection').attr("id"));

		  var typeName = treeNode.name;
		  //$(".main-iframe").attr('src',ctx + '/DataLink/get/group/classify/'+id+'.do?typeName='+typeName);
          //$(".main-iframe").attr('src',ctx + '/DataLink/get/group/classify/id/typeName');
          $(".main-iframe").attr('src','/ds/catalog/get/group/'+id);
	  } else {
		  var id = treeNode.data_id;
          console.log('js文件id');
          console.log(id);
	      var zTree = $.fn.zTree.getZTreeObj('main_left_tree');
	      var nodes = zTree.getSelectedNodes()[0];
	      zTree.expandNode(treeNode, null, null, null, true);
	      //$("#main-iframe").attr('src',ctx + '/DataLink/edit/' + id);
          $("#main-iframe").attr('src','/ds/edit/data/'+id);
	  }
  }

  function addDiyDom(treeId, treeNode) {
    var spaceWidth = 25;
    var switchObj = $("#" + treeNode.tId + "_switch"),
      icoObj = $("#" + treeNode.tId + "_ico");
    switchObj.remove();
    icoObj.before(switchObj);
    if (treeNode.level > 0) {
      var spaceStr = "<span class='spaceSpan' style='width:" + (spaceWidth * treeNode.level) + "px'></span>";
      switchObj.before(spaceStr);
    }

    if (treeId == 'main_left_tree') {
      var aObj2 = $('#' + treeNode.tId + '_a');
      var moreStr = '<span class="iconBtn moreBtn popout-btn popout-mainLeftTree-btn" title="更多"></span>';
      aObj2.after(moreStr);
    }
  }

  function saveDatalinkType(treeId, treeNode, newName, isCancel) {
	newName = newName.trim();
    if (newName === '') {
      pop_info("名称不能为空");
     // $('.main-l-b-tree .newFolder').addClass('disabled');
      var zTree = $.fn.zTree.getZTreeObj(treeId);
      //zTree.editName(treeNode);
      zTree.removeNode(treeNode);
      return false;
    } else {
      $('.main-l-b-tree .newFolder').removeClass('disabled');
      var result = true;
      //var url = "/DataLink/add/classify.do";
      var url = "/ds/catalog/create";
      $.ajax({
      	url : url,
      	data:{name:newName},
          async : false,
          type : "POST",
          dataType : 'json',
          success : function (data){
          	if(data.code==0) {
                  pop_succeed("添加成功");
                  loadTree("common");
                  //添加新分类后 编辑页面同步刷新下拉框
                  var obj=document.getElementById("main-iframe").contentWindow;
                  var ifmObjFile=obj.document.getElementById("isEditPageFile");

                  var ifmObjDB=obj.document.getElementById("isEditPageDB");
                  console.log(ifmObjFile);
                  //console.log(ifmObjFile.value);
                  if(ifmObjFile!=null && ifmObjFile.value=='true'){
                      console.log("往下更新下拉框")
                	  var html=obj.document.getElementById('fileClassifySelect').innerHTML;
                      console.log(html);
                       html+=('<option value="'+data.id+'">'+newName+'</option>');
                       console.log(html);
                       obj.document.getElementById('fileClassifySelect').innerHTML = html;
                       obj.layui.form.render();
                  }else if(ifmObjDB!=null && ifmObjDB.value=='true'){
                	  var html=obj.document.getElementById('classifySelect').innerHTML;
                      html+=('<option value="'+data.id+'">'+newName+'</option>');
                      obj.document.getElementById('classifySelect').innerHTML = html;
                      obj.layui.form.render();
                  }
              }else{
                pop_info(data.msg);
                result = false;
              }
          }
      });
      return result;
    }
  }

  function mainLeft2OnClick(event, treeId, treeNode) {
    console.log(event, treeId, treeNode);
  };

  var setting_mainLeft1 = {
    view: {
      showIcon: true,
      showLine: true,
      selectedMulti: false,
      dblClickExpand: false,
      addDiyDom: addDiyDom
    },
    edit: {
      enable: true,
      showRemoveBtn: false,
      showRenameBtn: false,
      drag: {
        isCopy: false,
        isMove: false
      }
    },
    data: {
      keep: {
        parent: true,
        leaf: false
      }
    },
    callback: {
      beforeRename: saveDatalinkType,
      onClick: onClick
    }
  };

  //var zNodes_mainLeft1 = [];

  //加载数据连接
  function queryDataLinks(){
      var type = $(".search-type .active").attr("value");
      var value = '';
      if('byName' == type){
      	value = $("div[sel-cont='type1']").find(":input").val();
      	if(value != null){
      		value = $.trim(value);//滤前后空格
      		$("div[sel-cont='type1']").find(":input").val(value);
      	}
      }else if('byUser' == type){
      	value = $("div[sel-cont='type2']").find("li.active").attr("value") || '';
      }else if('byType' == type){
      	value = $("div[sel-cont='type3']").find("li.active").attr("value") || '';
      }

      /* $(".main-iframe").attr('src',ctx + '/DataLink/Index.do?type=' + type +"&value=" + value); */
      $(".main-iframe").attr('src','ds/get/data_list');//ds/catalog/get/data/info
  }

  function loadClassifyDown(list, classifyId) {
      $('select[name=classify_select]').empty();
	  //var option_str = "<option value=''>请选择</option>";
      var option_str = "";
	  if (list != null && list.length > 0) {
          for (var i = 0; i < list.length > 0; i++) {
              var classify = list[i];
              var selectedClass = classifyId == classify['id'] ? "selected" : "";
              option_str += "<option value='" + classify['id'] + "' " +selectedClass + ">" + classify['name'] + "</option>";
          }
          $('select[name=classify_select]').append(option_str);
          layui.form.render('select');
      }
  }

/*   var zNodes_mainLeft1 = [{
    name: '默认目录',
    children: [{
      iconSkin: 'excel',
      name: 'excel1'
    }, {
      iconSkin: 'excel',
      name: 'excel2'
    }]
  }]; */

  //加载分类数
  function loadTree(chartType){
	console.log("加载分类数");
	var type = $(".search-type .active").attr("value");
    var value = '';
    if('byName' == type){
    	value = $("div[sel-cont='type1']").find(":input").val();
    	if(value != null){
    		value = $.trim(value);//滤前后空格
    		$("div[sel-cont='type1']").find(":input").val(value);
    	}
    }else if('byUser' == type){
    	value = $("div[sel-cont='type2']").find("li.active").attr("value") || '';
    }else if('byType' == type){
    	value = $("div[sel-cont='type3']").find("li.active").attr("value") || '';
    }
	//加载数据连接分类
  	//var url = ctx+"/DataLink/get/menu.do?value="+value+"&type="+type+"&searchByName="+chartType;
  	var url = "/ds/catalog/get/menu";
    //$.ajaxSettings.async = false;
  	$.get(url,function (data) {
        var data = data.data;
        console.log(data);
  		var zNodes_mainLeft1 = [];
          for(var pro in data){
              var dataLinks = data[pro].child;
        	  for(var i=0; i < dataLinks.length; i++){
	          		var iconSkin = 'excel';
                    if (dataLinks[i].data_type == null){
                        dataLinks[i].iconSkin = 'txt';
                    }else if(dataLinks[i].data_type.toLowerCase() == 'csv'){
                        dataLinks[i].iconSkin = dataLinks[i].data_type.toLowerCase();
                    }else{
                        dataLinks[i].iconSkin = 'excel'
                    }
	          		//dataLinks[i].iconSkin = dataLinks[i].data_type == null ? 'txt' : dataLinks[i].data_type.toLowerCase();
	          };
              var c = {
                  name:data[pro].name,
                  //click:"$('#rightContent')[0].contentWindow.app.queryClassify('" + data[pro].id + "')",
                  //children: buildList(dataLinks),
                  children: dataLinks,
                  isParent:true,
                  dataId:data[pro].catalog_id
              };
              zNodes_mainLeft1.push(c); 
          }
          if ($('.ztree').hasClass('ztree1')) {
          	$.fn.zTree.init($('#main_left_tree'), setting_mainLeft1, zNodes_mainLeft1);
          	
          	window.mainLeftZtree = $.fn.zTree.getZTreeObj('main_left_tree');
          	if("SearchByName" == chartType && ""!=value){
          		$.fn.zTree.getZTreeObj('main_left_tree').expandAll(true);
            }
          }
          
          //加载分类下拉
          //loadClassifyDown(zNodes_mainLeft1);
          
          //直接打开数据连接信息
          /*if(dataLinkId1 !=null && dataLinkId1 !=""){
	    		var zTree = $.fn.zTree.getZTreeObj('main_left_tree');
	            var treeNode =zTree.getNodeByParam("id",dataLinkId1 );
	            onClick(null, 'main_left_tree', treeNode)
	            zTree.setting.callback.onClick(zTree.selectNode(treeNode),
	              		'main_left_tree', treeNode);
          }*/
      })
  }
  
  queryDataLinks();
  
  function buildList(list) {
	    var contain = [],data = list;
	    if (list != null) {
	        for(var pro in data){
	            var c = {
	                name:data[pro].name,
	                //click:"$('#rightContent')[0].contentWindow.app.queryChart('"+data[pro].id+"')",
	                dataId:data[pro].id
	            };
	            contain.push(c);
	        }
	    }
	    return contain;
	}
  loadTree("common");

  //main-l ztree重命名
  $(document).on('click', '#mainLeftTree_rename', function(e) {
    var zTree = $.fn.zTree.getZTreeObj('main_left_tree');
    var treeNode = zTree.getNodeByTId(mainLeftTree);
    var treeNodeName = treeNode.name;

    $('.pop-cont-mainLeftTreeRename').removeClass('hide');
    var _this = $(e.target);
    
    var isClassify = treeNode.isParent;
    var datalinkId = treeNode.data_id;
    var classifyId = treeNode.dataId
    layer.open({
        type: 1,
        title: '重命名',
        skin: 'layer-over mainLeftTreeRename',
        area: ['280px', 'auto'], //宽高
        content: $('.pop-cont-mainLeftTreeRename'),
        btn: ['取消', '确定'],
        btn2: function(index1, layero1) {
            var filename = $.trim($('.mainLeftTreeRename input').val());
            if (filename.length > 0) {
                if(treeNodeName==filename){
                    pop_info(filename + "与原名相同...");
                    return false;
                }
                if($.trim(filename) != ""){
                    /* var url = isClassify ? ctx+"/DataLink/update/classify/name.do" : ctx+"/DataLink/rename/" + datalinkId; */
                    console.log(treeNodeName);
                    console.log(datalinkId);
                    console.log(isClassify);
                    console.log(classifyId);
                    var url = isClassify ? "/ds/catalog/modify" :"/ds/rename/data/"+datalinkId;
                    console.log(url);
                    parm={catalog_id:classifyId, name:filename};
                    
                    $.post(url,parm,function (data) {
                        //var data = JSON.parse(data);
                        console.log(data);
                        if(data.code==0 || data.msg == 'SUCCESS'){
                        	treeNode.name = filename;
                            zTree.updateNode(treeNode);
                        	pop_succeed("修改成功");
                            //okAction("修改成功");
                            //修改类型名字后刷新编辑页面下拉框
                            var obj=document.getElementById("main-iframe").contentWindow;
                            var ifmObjFile=obj.document.getElementById("isEditPageFile"); 
                            var ifmObjDB=obj.document.getElementById("isEditPageDB"); 
                            if(ifmObjFile!=null && ifmObjFile.value=='true'){
                            	var select=obj.document.getElementById('fileClassifySelect');
                            	var option=$("option[value="+parm.id+"]",select);
                            	if(option[0]){
                                  option[0].innerText=filename;
                                }
                            	obj.layui.form.render();
                            }else if(ifmObjDB!=null && ifmObjDB.value=='true'){
                            	var select=obj.document.getElementById('classifySelect');
                            	var option=$("option[value="+parm.id+"]",select);
                                if(option[0]){
                                  option[0].innerText=filename;
                                }
                                obj.layui.form.render();
                            }

                            //左侧树 数据连接重命名 右侧即时更新
                            var iframeSrc = $(".main-iframe").attr('src');
                            if (iframeSrc.indexOf("DataLink/edit/" + treeNode.id) > -1) {
                              $(".main-iframe").contents().find(".main-r-t .title .tit").text(filename);
                              $(".main-iframe").contents().find(".layui-input-block .chakan").text(filename);
                            } else if (iframeSrc.indexOf("DataLink/Index.do") > -1 || iframeSrc.indexOf("DataLink/get/group") > -1) {
                              $(".main-iframe").attr('src',iframeSrc);
                            }
                        } else if (data.code==-1) {
                            pop_failure(data.msg);
                        } else if(data.code==1){
                            pop_info(data.msg);
                        }else if(data.msg == 'INUSE'){
                    		pop_info("名称重复，请重新输入");
                    	} else if(data.msg == 'ERROR' || data.msg == 'NOTFOUND'){
                    		pop_failure("内部错误，请稍后再试！");
                    	}
                    })
                }else{
                    pop_info("分类名称不能为空");
                }
            } else {
                pop_info("名称不能为空");
                return false;
            }
        },
        end: function(index1, layero1) {
            $('.pop-cont-mainLeftTreeRename input').val('');
            $('.pop-cont-mainLeftTreeRename').addClass('hide');
        }
    });
    $('.mainLeftTreeRename input').val(treeNodeName);
  });

  //main-l ztree删除
  $(document).on('click', '#mainLeftTree_del', function(e) {
    var zTree = $.fn.zTree.getZTreeObj('main_left_tree');
    var treeNode = zTree.getNodeByTId(mainLeftTree);
    if (treeNode.isParent) {
    	layer.confirm("确认删除该分类？" ,{
    	 title:"删除",
   		 btn: ['取消','确定'],
   	     btn2: function(index, layero) {
               
   	    	    parm={ id : treeNode.dataId};
                console.log(parm);
               //$.post(ctx+"/DataLink/del/classify.do",{ id : treeNode.dataId },function (data) 
               $.post("/ds/catalog/delete",{ catalog_id : treeNode.dataId },function (data) {
                   if(data.result == 0){
                      pop_failure("删除失败！");
                   }else if(data.result == 1){
                       //删除类别后，更新编辑页面下拉框
                       var obj=document.getElementById("main-iframe").contentWindow;
                       var ifmObjFile=obj.document.getElementById("isEditPageFile"); 
                       var ifmObjDB=obj.document.getElementById("isEditPageDB"); 
	                       if(ifmObjFile!=null && ifmObjFile.value=='true'){
	                       	var select=obj.document.getElementById('fileClassifySelect');
	                       	var option=$("option[value="+parm.id+"]",select);
	                       	option.remove();
	                            obj.layui.form.render();
	                       }else if(ifmObjDB!=null && ifmObjDB.value=='true'){
	                       	var select=obj.document.getElementById('classifySelect');
	                       	var option=$("option[value="+parm.id+"]",select);
	                       		option.remove();
	                           obj.layui.form.render();
	                       }
	                       loadTree("common");
	                       pop_succeed("删除成功");
                   }else  if(data.result == 2){
                       pop_info("该分类下存在数据连接!")
                   }
               })
           },
           end:function () {

           }
       })
    } else {
      layer.confirm('确认删除该数据连接？', {
        title:"删除",
        btn: ['取消', '确定'],
        btn2: function(index, layero) {
    		//var url = ctx + '/DataLink/delete/' + treeNode.id;
            var url = '/ds/delete/data/'+treeNode.data_id;
            $.ajax({
                url : url,
                type : 'POST',
                dataType : 'json',
                success : function(msg){
                	if(msg.msg == 'SUCCESS'){
                		pop_succeed("删除成功！");
                		//var url = ctx + '/DataLink/get/group/classify/'+treeNode.getParentNode().id+'.do'
                		//var iframeSrc = $(".main-iframe").attr('src');
                		zTree.removeNode(treeNode);
                		/*if(iframeSrc.indexOf('/DataLink/get/group/classify/') > -1){
                			$(".main-iframe").attr('src',iframeSrc);
                		}*/
                		updateDataLinkListPageIndex();
                	}else if(msg.msg == 'INUSE'){
                		pop_info("已用于创建数据主题，不能删除");
                	}else if(msg.msg == 'ERROR' || msg.msg == 'NOTFOUND'){
                		pop_failure("内部错误，请稍后再试！");
                	}
                }
            });  
        }
      });
    }
  });

  function updateDataLinkListPageIndex(){
      var type = $(".search-type .active").attr("value");
      var value = '';
      if('byName' == type){
      	value = $("div[sel-cont='type1']").find(":input").val();
      }else if('byUser' == type){
      	value = $("div[sel-cont='type2']").find("li.active").attr("value") || '';
      }else if('byType' == type){
      	value = $("div[sel-cont='type3']").find("li.active").attr("value") || '';
      }
      $(".main-iframe").attr('src',ctx + '/DataLink/Index.do?type=' + type +"&value=" + value);
  }
  
  function okAction(msg) {
	    layer.msg(msg);
	    setTimeout(function () {
	        //loadTree();
	        window.location.reload(true)
	        layer.closeAll();
	    },1500);
	}
  
  function newFolder(treeID) {
    var zTree = $.fn.zTree.getZTreeObj(treeID);
    var newNode = {
      name: '',
      isParent: true
    };
    var treeNode = zTree.addNodes(null, newNode);
    zTree.editName(treeNode[0]);
  }
  

  //main-l-b-tree新建文件夹
  $('.main-l-b-tree .newFolder').click(function(e) {
    if (!$(this).hasClass('disabled')) {
      var _this = $(this);
      if (!_this.parents('.layui-colla-item').find('.layui-colla-content').hasClass('layui-show')) {
        _this.parents('.layui-collapse').find('.layui-colla-content').removeClass('layui-show');
        _this.parents('.layui-colla-item').find('.layui-colla-content').addClass('layui-show');
      }

      var treeID = _this.parents('.layui-colla-item').find('.ztree').attr('id');
      newFolder(treeID);
    }
    e.stopPropagation();
  });

  //main-l-b-tree点击标题
  $('.main-l-b-tree .title-name').click(function(e) {
    e.stopPropagation();
    //console.log('全部');
    queryDataLinks();
	loadTree("SearchByName");
  });

  //新建数据连接
  $(document).on('click', '.pop-addDataConnection', function(e) {
    $('.pop-cont-addDataConnection').removeClass('hide');
    layer.open({
      type: 1,
      title: '新建数据连接',
      area: ['660px', 'auto'], //宽高
      content: $('.pop-cont-addDataConnection'),
      success: function(layero){
          $(".layui-layer-page").css("z-index","198910151");
      },
      end: function(index1, layero1) {
        $('.pop-cont-addDataConnection').addClass('hide');
        $(".layui-layer-shade").css("display","none");

      }
    });
  });

  //数据库连接 查看数据
  window.viewData = function() {
    $('.pop-cont-viewData').removeClass('hide');
    layer.open({
      type: 1,
      title: 't_user1',
      area: ['800px', '600px'], //宽高
      content: $('.pop-cont-viewData'),
      btn: ['取消', '确定'],
      btn2: function(index1, layero1) {

      },
      end: function(index1, layero1) {
        $('.pop-cont-viewData').addClass('hide');
      }
    });
    //初始化table
    table.render({
      elem: '#table_demo7',
      height: 'full-190',
      text: {
        none: '暂无数据'
      },
      data: [
        { "id": 10000, "field1": "广州", "field2": 100, "field3": 200, "field4": 300, "field5": "2018-01-01" },
        { "id": 10001, "field1": "中山", "field2": 101, "field3": 201, "field4": 301, "field5": "2018-01-01" },
        { "id": 10002, "field1": "深圳", "field2": 102, "field3": 202, "field4": 302, "field5": "2018-01-02" },
        { "id": 10003, "field1": "佛山", "field2": 103, "field3": 203, "field4": 303, "field5": "2018-01-03" }
      ],
      cols: [
        [
          { field: 'field1', title: '<i class="icon icon-sjy-abc"></i>区域', sort: true },
          { field: 'field2', title: '<i class="icon icon-sjy-123"></i>总人口(万人)', sort: true },
          { field: 'field3', title: '<i class="icon icon-sjy-123"></i>男性人口(万人)', sort: true },
          { field: 'field4', title: '<i class="icon icon-sjy-123"></i>女性人口(万人)', sort: true },
          { field: 'field5', title: '<i class="icon icon-sjy-rili"></i>统计时间', sort: true },
        ]
      ],
      page: false
    });
  }

  //选择数据连接
  $(document).on('click', '.pop-addDataSubject', function() {
    $('.pop-cont-addDataSubject').removeClass('hide');
    layer.open({
      type: 1,
      skin: 'layer-over form-box1',
      title: '选择数据连接',
      area: ['600px', '480px'], //宽高
      content: $('.pop-cont-addDataSubject'),
      btn: ['取消', '确定'],
      btn2: function(index1, layero1) {

      },
      end: function(index1, layero1) {
        $('.pop-cont-addDataSubject').addClass('hide');
      }
    });
  });
  /*$(document).on('click', '.addDataSubject .cus-menulist dt .tit', function() {
    var fa = $(this).parents('dl');
    if (fa.hasClass('active')) {
      fa.removeClass('active');
    } else {
      fa.addClass('active').siblings('dl').removeClass('active');
    }
  });
  $(document).on('click', '.addDataSubject .cont-l .list li', function(e) {
    var _this = $(this),
      r_list = _this.parents('.addDataSubject').find('.cont-r .list');
    var num = _this.attr('data-num');
    if (_this.hasClass('active')) {
      _this.removeClass('active');
      if ($(r_list).find('li').length <= 1) {
        r_list.find('.list-none').removeClass('hide');
      }
      r_list.find('ul li[data-num=' + num + ']').remove();
    } else {
      _this.addClass('active');
      if ($(r_list).find('li').length <= 0) {
        r_list.find('.list-none').addClass('hide');
      }
      r_list.find('ul').append('<li data-num=' + num + '>' + _this.html() + '<div class="del"></div></li>');
    }
  });
  $(document).on('click', '.addDataSubject .cont-r .list li .del', function(e) {
    var _this = $(this),
      fa = _this.parents('li'),
      num = fa.attr('data-num'),
      l_list = _this.parents('.addDataSubject').find('.cont-l .list');
    l_list.find('ul li[data-num=' + num + ']').removeClass('active');
    fa.remove();
  });*/

  //选择数据主题
  $(document).on('click', '.pop-addDataSet', function() {
    $('.pop-cont-addDataSet').removeClass('hide');
    layer.open({
      type: 1,
      skin: 'layer-over form-box1',
      title: '选择数据主题',
      area: ['400px', '480px'], //宽高
      content: $('.pop-cont-addDataSet'),
      btn: ['取消', '确定'],
      btn2: function(index1, layero1) {

      },
      end: function(index1, layero1) {
        $('.pop-cont-addDataSet').addClass('hide');
      }
    });
  });
  $(document).on('click', '.addDataSet .list li', function(e) {
    $(this).addClass('active').siblings('li').removeClass('active');
  });

  //添加自定义SQL视图
  window.customSQL = function() {
    $('.pop-cont-customSQL').removeClass('hide');
    layer.open({
      type: 1,
      title: '自定义SQL视图',
      area: ['600px', '380px'], //宽高
      content: $('.pop-cont-customSQL'),
      btn: ['取消', '确定'],
      btn2: function(index1, layero1) {

      },
      end: function(index1, layero1) {
        $('.pop-cont-customSQL').addClass('hide');
      }
    });
  }

  // 文本文件上传弹窗
  $(document).on('click', '.new-showPopTxtBtn', function(e) {
    $('.pop-cont-txtUpload').removeClass('hide');
    layer.open({
      type: 1,
      skin: 'layer-over form-box1 form-dingshiset',
      title: '文本文件上传',
      area: ['400px', '270px'], //宽高
      content: $('.pop-cont-txtUpload'),
      btn: ['取消', '确定'],
      btn2: function(index1, layero1) {

      },
      end: function(index1, layero1) {
        $('.pop-cont-txtUpload').addClass('hide');
      }
    });
  })

  // 数据主题编辑页面
  // 定时设置弹窗
  $(document).on('click', '.timing-set', function(e) {
    $('.pop-cont-timeSetting').removeClass('hide');
    layer.open({
      type: 1,
      skin: 'layer-over form-box1 form-dingshiset',
      title: '定时设置',
      area: ['600px', '480px'], //宽高
      content: $('.pop-cont-timeSetting'),
      btn: ['取消', '确定'],
      btn2: function(index1, layero1) {

      },
      end: function(index1, layero1) {
        $('.pop-cont-timeSetting').addClass('hide');
      },
    });
  });

  // 时间选择弹窗
  // 开始日期
  laydate.render({
    elem: '#startDate' //指定元素
  });
  // 结束日期
  laydate.render({
    elem: '#endDate' //指定元素
  });

  //详情弹窗
  window.detailsPop = function() {
    $('.pop-cont-details').removeClass('hide');
    layer.open({
      type: 1,
      title: '失败详情',
      area: ['600px', 'auto'], //宽高
      content: $('.pop-cont-details'),
      btn: ['取消', '确定'],
      btn2: function(index1, layero1) {
    	  saveRole(roleId);
      },
      end: function(index1, layero1) {
        $('.pop-cont-details').addClass('hide');
      },
    });
  }
  
  //新增分类 addClassify
  $("#addClassify").click(function (e) {
	     $('#new-type').removeClass("hide");
	     $("#name").val("");
	     var pop_addClassify =
	     layer.open({
	         type:1,
	         title:"添加数据连接分类",
	         area: ['300px', 'auto'],
	         content:$('#new-type'),
	         btnAlign: 'c',
	         btn:["取消","确定"],
	         btn2:function (index) {
	             var val = $("#name").val();
	             if($.trim(val)!=""){
	                 var layerId = pop_running("添加中");
	                 $.post(ctx+"/DataLink/add/classify.do",{name:val},function (data) {
	                     if(data.code==0){	                         
	                      $('#select_classifies').prepend("<option value="+data.id+" selected>"+val+"</option>");		
     					  pop_succeed("添加成功");
	                     } else if (data.code == 1) {
	                         pop_info(data.msg);
	                     } else {
	                         //pop_failure(data.msg);
	                    	 pop_info(data.msg);
	                     }
	                 })
	             }else{
	                 pop_info("分类名称不能为空");
	             }
	         }
	     });
	 })

  //修改分类
  $(document).on('click', '.pop-addToCategory', function(e) {
	var zTree = $.fn.zTree.getZTreeObj('main_left_tree');
	var treeNode = zTree.getNodeByTId(mainLeftTree);
	var datalinkId = treeNode.id;
	var classifyId = treeNode.classify.id;
	
	//loadClassifyDown(zNodes_mainLeft1, classifyId);
	//var url = ctx + "/DataLink/get/menuSelect.do";
    var url = "/ds/get/menuselect";
    $.ajax({
    	url:url,
    	async: false,
    	success:function(data){
            console.log();
    		//加载分类下拉
            loadClassifyDown(data, classifyId);
    	}
    });
    $('.pop-cont-addToCategory').removeClass('hide');
    
	$('.pop-cont-addToCategory').removeClass('hide');
    var addToCategory = layer.open({
      type: 1,
      skin: 'layer-over',
      area: ['440px', 'auto'],
      title: '数据连接分类修改',
      content: $('.pop-cont-addToCategory'),
      btnAlign: 'c',
      btn: ['取消', '确定'],
      yes:function(){
    	   loadTree();
    	   layer.close(addToCategory);
       },
      btn2: function(index1,layero1){
          return updateClassify(datalinkId);
      },
      end: function() {
        $('.pop-cont-addToCategory').addClass('hide');
      }
    });
  });

  //更新
  function updateClassify(dataLinkId) {
	  var classifyId = $('select[name=classify_select]').val();
	  if(classifyId){
		  //var url = ctx+"/DataLink/datalink/update.do";
   		  var url = "/ds/subdirectory/data";

          $.post(url,{data_link_id:dataLinkId, catalog_id:classifyId},function (data) {
	          if(data.code==0){
	        	  loadTree("common");
	              okAction("修改成功");
	          }else{
	              layer.msg(data.msg);
	          }
	      })
	  }else{
		  layer.msg("请选择分类",{icon:8});
		  return false;
	  }
  }
  
 /* function refreshTree(){
	  loadTree("common");
  }
  */
  
  exports('dataLink_index', {});

});
