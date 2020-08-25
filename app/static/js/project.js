layui.define(['element', 'layer', 'form'], function(exports) {

    var $ = layui.jquery,
        element = layui.element,
        layer = layui.layer,
        form = layui.form;

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
            $('.pro-manage-tree').getNiceScroll().resize();
        }
    }

    function onClick(e, treeId, treeNode) {
        var zTree = $.fn.zTree.getZTreeObj(treeId);
        var nodes = zTree.getSelectedNodes()[0];

        if (treeId == 'sel_gcml_tree') {
            $('#sel_gcml_tree').find('li').removeClass('active');
            $('#' + nodes.tId).addClass('active');
            var str = $('#' + nodes.tId).find('.node_name').html();
            $('#sel_gcml .cus-select-btn').removeClass('cus-select-tips').html(str);
            $('.cus-select').removeClass('cus-selected');
        }

        if (treeId == 'pro_manage_tree') {
            zTree.expandNode(treeNode, null, null, null, true);
        }
    }

    function addDiyDom(treeId, treeNode) {
        if (treeId == 'sel_gcml_tree') {
            var aObj1 = $('#' + treeNode.tId);
            if (treeNode.rootNode) {
                var addFolderStr = '<span class="iconBtn addFolderBtn addFolderBtn-Root" title="创建目录"></span>';
            } else {
                var addFolderStr = '<span class="iconBtn addFolderBtn" title="创建目录"></span>';
            }
            aObj1.append(addFolderStr);

            var spaceWidth = 10;
            var switchObj = $("#" + treeNode.tId + "_switch"),
                icoObj = $("#" + treeNode.tId + "_ico");
            switchObj.remove();
            icoObj.before(switchObj);
            console.log(treeNode.level);
            if (treeNode.level > 0) {

                var spaceStr = "<span style='display: inline-block;width:" + (spaceWidth * treeNode.level) + "px'></span>";
                switchObj.before(spaceStr);
            }
        }
        if (treeId == 'pro_manage_tree') {
            var aObj2 = $('#' + treeNode.tId + '_a');
            var moreStr = '<span class="iconBtn moreBtn popout-btn popout-proTree-btn" title="更多"></span>';
            aObj2.after(moreStr);
        }
    }

    function addNode(rootFlag, isParentFlag, folderName, nodeId) {
        var zTree = $.fn.zTree.getZTreeObj('sel_gcml_tree');
        var treeNode = zTree.getNodeByTId(nodeId);
        var newNode = {
            name: folderName,
            isParent: isParentFlag
        };

        if (rootFlag) {
            zTree.addNodes(null, newNode);
        } else {
            zTree.addNodes(treeNode, newNode);
        }

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
    }

    var setting = {
        view: {
            showIcon: false,
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
            beforeExpand: beforeExpand,
            beforeClick: beforeClick,
            onExpand: onExpand,
            onClick: onClick
        }
    };

    var zNodes_1 = [{
        name: '我的工程',
        rootNode: true,
        click: false
    }, {
        name: '广西电信1',
        children: [{
            name: 'iPTV',
            children: [{
                name: '资源线性预测',
                isParent: true
            }, {
                name: '聚类',
                isParent: true
            }]
        }, {
            name: '数字电视',
            isParent: true
        }, {
            name: '宽带业务',
            isParent: true
        }]
    }, {
        name: '广西电信22222222222222222222222222222222222222',
        children: [{
            name: 'iPTV',
            children: [{
                name: '资源线性预测',
                isParent: true
            }, {
                name: '聚类',
                isParent: true
            }]
        }, {
            name: '数字电视',
            isParent: true
        }, {
            name: '宽带业务',
            isParent: true
        }]
    }, {
        name: '我的工程111111111111111111111111111111111111111',
        isParent: true
    }];

    var zNodes_2 = [{
        name: '广西电信1',
        isParent: true,
        children: [{
            name: 'iPTV',
            isParent: true,
            children: [{
                name: '资源线性预测'
            }, {
                name: '聚类'
            }]
        }, {
            name: '数字电视'
        }, {
            name: '宽带业务'
        }]
    }, {
        name: '广西电信2',
        isParent: true,
        children: [{
            name: 'iPTV',
            isParent: true,
            children: [{
                name: '资源线性预测'
            }, {
                name: '聚类'
            }]
        }, {
            name: 'iPTV',
            isParent: true,
            children: [{
                name: '资源线性预测'
            }, {
                name: '聚类'
            }]
        }]
    }];

    $(document).on('click', '.pro-manage-add', function() {
        $('.pro-cont-proManageAdd').removeClass('hide');
        layer.open({
            type: 1,
            title: '创建工程',
            skin: 'layer-over proManageAdd',
            area: ['400px', 'auto'], //宽高
            content: $('.pro-cont-proManageAdd'),
            btn: ['取消', '确定'],
            btn2: function(index1, layero1) {
                var item1 = $.trim($('.pro-cont-proManageAdd .layui-form-item1 input').val()),
                    item2 = $.trim($('.pro-cont-proManageAdd .layui-form-item2 textarea').val()),
                    item3 = $('.pro-cont-proManageAdd .layui-form-item3 .cus-select-btn').html(),
                    item4 = $('.pro-cont-proManageAdd .layui-form-item4 select').val(),
                    item5 = $('.pro-cont-proManageAdd .layui-form-item5 select').val();
                if (item1 == '' || item3 == '' || item4 == null || item5 == null) {
                    if (item1 == '') {
                        layer.msg('工程名称不能为空', { icon: 8 });
                    } else if (item3 == '') {
                        layer.msg('工程目录不能为空', { icon: 8 });
                    } else if (item4 == null) {
                        layer.msg('算法模板不能为空', { icon: 8 });
                    } else if (item5 == null) {
                        layer.msg('数据集不能为空', { icon: 8 });
                    }
                    return false;
                } else {
                    console.log(item1, item2, item3, item4, item5);
                    $('.pro-cont-proManageAdd .layui-form-item1 input,.pro-cont-proManageAdd .layui-form-item2 textarea,.pro-cont-proManageAdd .layui-form-item4 select,.pro-cont-proManageAdd .layui-form-item5 select').val('');
                    $('.pro-cont-proManageAdd .layui-form-item3 .cus-select-btn').html('');
                    var zTree = $.fn.zTree.getZTreeObj('sel_gcml_tree');
                    zTree.cancelSelectedNode();
                }
            },
            end: function(index1, layero1) {
                $('.pro-cont-proManageAdd').addClass('hide');
            }
        });
        form.render('select', 'proManageAddForm');
        $('.pro-cont-proManageAdd .layui-select-tips').addClass('layui-disabled');
        $.fn.zTree.init($('#sel_gcml_tree'), setting, zNodes_1);

        //select添加自定义图标
        $('.layui-select-style2 option').each(function(index, domEle) {
            var icon = $(this).attr('data-icon');
            $(this).parents('.layui-select-style2').find('dd').eq(index).addClass(icon);
        });
    });

    $(document).on('click', '.addFolderBtn', function(e) {
        $('.pro-cont-proFolderAdd').removeClass('hide');
        var _this = $(e.target);
        var rootFlag = _this.hasClass('addFolderBtn-Root'),
            isParentFlag = true,
            nodeId = e.target.parentNode.id;
        layer.open({
            type: 1,
            title: '创建目录',
            skin: 'layer-over proFolderAdd',
            area: ['280px', 'auto'], //宽高
            content: $('.pro-cont-proFolderAdd'),
            btn: ['取消', '确定'],
            btn2: function(index1, layero1) {
                var folderName = $.trim($('.proFolderAdd input').val());
                if (folderName.length > 0) {
                    addNode(rootFlag, isParentFlag, folderName, nodeId);
                } else {
                    layer.msg('目录名称不能为空', { icon: 8 });
                    return false;
                }
            },
            end: function(index1, layero1) {
                $('.pro-cont-proFolderAdd input').val('');
                $('.pro-cont-proFolderAdd').addClass('hide');
            }
        });
    });

    $.fn.zTree.init($('#pro_manage_tree'), setting, zNodes_2);

    var popoutBtnId;
    $(document).on('click', '.popout-proTree-btn', function(e) {
        e.stopPropagation();
        popoutBtnId = e.target.parentNode.id;
        $('.popout-proTree-btn').removeClass('active');
        $(this).addClass('active');
        var left = e.pageX + 5,
            top = e.pageY + 10;
        $('.popout-proTree').addClass('active').css({
            'left': left,
            'top': top
        });
        return false;
    });

    //编辑
    $(document).on('click', '#pro_manage_tree_edit', function(e) {
        var zTree = $.fn.zTree.getZTreeObj('pro_manage_tree');
        var treeNode = zTree.getNodeByTId(popoutBtnId);
        var treeNodeName = treeNode.name;

        if (treeNode.isParent) {
            $('.pro-cont-proFolderAdd').removeClass('hide');
            var _this = $(e.target);
            layer.open({
                type: 1,
                title: '编辑目录',
                skin: 'layer-over proFolderAdd',
                area: ['280px', 'auto'], //宽高
                content: $('.pro-cont-proFolderAdd'),
                btn: ['取消', '确定'],
                btn2: function(index1, layero1) {
                    var folderName = $.trim($('.proFolderAdd input').val());
                    if (folderName.length > 0) {
                        treeNode.name = folderName;
                        zTree.updateNode(treeNode);
                    } else {
                        layer.msg('目录名称不能为空', { icon: 8 });
                        return false;
                    }
                },
                end: function(index1, layero1) {
                    $('.pro-cont-proFolderAdd input').val('');
                    $('.pro-cont-proFolderAdd').addClass('hide');
                }
            });
            $('.proFolderAdd input').val(treeNodeName);
        } else {
            $('.pro-cont-proManageAdd').removeClass('hide');
            layer.open({
                type: 1,
                title: '编辑工程',
                skin: 'layer-over proManageAdd',
                area: ['400px', 'auto'], //宽高
                content: $('.pro-cont-proManageAdd'),
                btn: ['取消', '确定'],
                btn2: function(index1, layero1) {
                    var item1 = $.trim($('.pro-cont-proManageAdd .layui-form-item1 input').val()),
                        item2 = $.trim($('.pro-cont-proManageAdd .layui-form-item2 textarea').val()),
                        item3 = $('.pro-cont-proManageAdd .layui-form-item3 .cus-select-btn').html(),
                        item4 = $('.pro-cont-proManageAdd .layui-form-item4 select').val(),
                        item5 = $('.pro-cont-proManageAdd .layui-form-item5 select').val();
                    if (item1 == '' || item3 == '' || item4 == null || item5 == null) {
                        if (item1 == '') {
                            layer.msg('工程名称不能为空', { icon: 8 });
                        } else if (item3 == '') {
                            layer.msg('工程目录不能为空', { icon: 8 });
                        } else if (item4 == null) {
                            layer.msg('算法模板不能为空', { icon: 8 });
                        } else if (item5 == null) {
                            layer.msg('数据集不能为空', { icon: 8 });
                        }
                        return false;
                    } else {
                        treeNode.name = item1;
                        zTree.updateNode(treeNode);
                    }
                },
                end: function(index1, layero1) {
                    $('.pro-cont-proManageAdd').addClass('hide');
                }
            });
            $('.layui-form-item1 input').val(treeNodeName);
            form.render('select', 'proManageAddForm');
            $('.pro-cont-proManageAdd .layui-select-tips').addClass('layui-disabled');
            $.fn.zTree.init($('#sel_gcml_tree'), setting, zNodes_1);
        }
    });

    //删除
    $(document).on('click', '#pro_manage_tree_del', function(e) {
        var zTree = $.fn.zTree.getZTreeObj('pro_manage_tree');
        var treeNode = zTree.getNodeByTId(popoutBtnId);
        if (treeNode.isParent) {
            if (treeNode.children) {
                if (treeNode.children.length > 0) {
                    layer.msg('不能删除，请先清空该目录下所有工程', { icon: 8 });
                } else {
                    layer.confirm('是否确认删除目录？', {
                        btn: ['取消', '确定'],
                        btn2: function(index, layero) {
                            zTree.removeNode(treeNode);
                        }
                    });
                }
            } else {
                layer.confirm('是否确认删除目录？', {
                    btn: ['取消', '确定'],
                    btn2: function(index, layero) {
                        zTree.removeNode(treeNode);
                    }
                });
            }
        } else {
            layer.confirm('是否确认删除工程？', {
                btn: ['取消', '确定'],
                btn2: function(index, layero) {
                    zTree.removeNode(treeNode);
                }
            });
        }
    });

    exports('project', {});

});
