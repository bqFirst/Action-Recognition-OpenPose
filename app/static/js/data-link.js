layui.define(['element', 'layer', 'table'], function(exports) {

    var $ = layui.jquery,
        element = layui.element,
        layer = layui.layer;
    	table = layui.table;

    $(document).on('click', '.data-link-delete', function(e) {
    	var id = $(this).attr("value");
       
    	var self = this;
        layer.confirm('是否确认删除此数据连接？', {
            title: "删除",
            btn: ['取消', '确定'],
            btn2: function(index, layero) {
            	//var url = ctx + '/DataLink/delete/' + id;
                var url = '/ds/delete/data/' + id;
                $.ajax({
                    url : url,
                    type : 'POST',
                    dataType : 'json',
                    success : function(msg){
                    	if(msg.msg == 'SUCCESS'){
                    		//更新数据连接导航树
                            var zTree = parent.mainLeftZtree;
                            var treeNode = zTree.getNodeByParam("id", id, null);
                            $(self).parents('tr').remove();
                            zTree.removeNode(treeNode);
                    		pop_succeed('删除成功！');
                    	}else if(msg.msg == 'INUSE'){
                    		pop_info('已用于创建数据主题，不能删除');
                    	}else if(msg.msg == 'ERROR' || msg.msg == 'NOTFOUND'){
                    		pop_failure('内部错误，请稍后再试！');
                    	}
                    }
                });                        		
            }
        });
    });
    
    exports('data-link', {});
});