
//数据连接导航树
var mainLeftZtree = null;


function chageSplitRadioValue(splitValue){
	$('#other').attr("disabled",true);
	$('#other').val('');
	if("other" == splitValue){
		$('#other').attr("disabled",false);
	}
}

layui.define(['element', 'layer'], function(exports) {

    var $ = layui.jquery,
        element = layui.element,
        layer = layui.layer,
        form = layui.form;

        form.on('radio(filter_split_radio)', function(data){
        	//console.log('split-类型.');
        	//console.log(data.elem); //得到radio原始DOM对象
        	//console.log(data.value); //被点击的radio的value值
        	chageSplitRadioValue(data.value);
        });



    function onClick(e, treeId, treeNode) {
        var zTree = $.fn.zTree.getZTreeObj('main_left_tree');
        var nodes = zTree.getSelectedNodes()[0];
        zTree.expandNode(treeNode, null, null, null, true);
        var id = treeNode.id;
        $(".main-iframe").attr('src',ctx + '/DataLink/edit/' + id);
    }


    function updateDataLinkListPage(){
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


    //跳转到新建数据库连接
    $(document).on('click', '.dbSelect', function(e) {
    	$('.pro-cont-addDataConnection').addClass('hide');
    	layer.closeAll();
    	var type = $(this).find(".text-b").attr("value");
    	if(type != undefined && type != null && type.length > 0){
    		$(".main-iframe").attr('src',ctx + '/DBDataLink/type/' + type);
    	}

    });

    exports('data-link-main', {});
});