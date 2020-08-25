function resizeFun() {
  //main-l-b-tree
  $('.main-l-b-tree .layui-colla-content').css({
    'height': $(window).height() - 60 - 104 - $('.main-l-b-tree .layui-colla-item').length * (30 + 2) + 'px'
  });
}
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


//修改数据类型
function tableColType(col) {
  console.log(col);
  $('.pop-cont-tableColType').removeClass('hide');
  layer.open({
    type: 1,
    skin: 'layer-over form-box1',
    title: '修改数据类型',
    area: ['300px', 'auto'], //宽高
    content: $('.pop-cont-tableColType'),
    btn: ['取消', '确定'],
    btn2: function(index1, layero1) {
      layer.msg($('.pop-cont-tableColType').find('select').val(), { icon: 9 });
    },
    end: function(index1, layero1) {
      $('.pop-cont-tableColType').addClass('hide');
    }
  });
}

//列重命名
function tableColRename(col) {
  console.log(col);
  $('.pop-cont-tableColRename').removeClass('hide');
  layer.open({
    type: 1,
    skin: 'layer-over form-box1',
    title: '列重命名',
    area: ['300px', 'auto'], //宽高
    content: $('.pop-cont-tableColRename'),
    btn: ['取消', '确定'],
    btn2: function(index1, layero1) {
      var val = $.trim($('.pop-cont-tableColRename').find('input').val());
      if (val == '') {
        layer.msg('列名不能为空', { icon: 8 });
        return false;
      } else {
        layer.msg(val, { icon: 9 });
      }
    },
    end: function(index1, layero1) {
      $('.pop-cont-tableColRename').find('input').val('');
      $('.pop-cont-tableColRename').addClass('hide');
    }
  });
}

//插入列
function tableAddCol() {
  $('.pop-cont-tableColRename').removeClass('hide');
  layer.open({
    type: 1,
    skin: 'layer-over form-box1',
    title: '插入列',
    area: ['300px', 'auto'], //宽高
    content: $('.pop-cont-tableColRename'),
    btn: ['取消', '确定'],
    btn2: function(index1, layero1) {
      var val = $.trim($('.pop-cont-tableColRename').find('input').val());
      if (val == '') {
        layer.msg('列名不能为空', { icon: 8 });
        return false;
      } else {
        layer.msg(val, { icon: 9 });
      }
    },
    end: function(index1, layero1) {
      $('.pop-cont-tableColRename').find('input').val('');
      $('.pop-cont-tableColRename').addClass('hide');
    }
  });
}

//删除行
function tableDelRow() {
  layer.confirm('确定删除选中的行？', {
    btn: ['取消', '确定'],
    btn2: function(index, layero) {
      layer.msg('点击了确定', { icon: 9 });
    }
  });
}

//删除列
function tableDelCol() {
  layer.confirm('确定删除选中的列？', {
    btn: ['取消', '确定'],
    btn2: function(index, layero) {
      layer.msg('点击了确定', { icon: 9 });
    }
  });
}

layui.define(['element', 'layer', 'form', 'table', 'laydate'], function(exports) {

  var $ = layui.jquery,
    element = layui.element,
    layer = layui.layer,
    form = layui.form,
    laydate = layui.laydate,
    table = layui.table;

  // 任务频率选择
  form.on('select(taskRate)', function(data) {
    var type = data.value;
    switch (type) {
      case 'hour':
        $('.hourBox').show().siblings('.taskRateBox').hide();
        break;
      case 'week':
        $('.weekBox').show().siblings('.taskRateBox').hide();
        break;
      case 'month':
        $('.monthBox').show().siblings('.taskRateBox').hide();
        break;
      case 'day':
        $('.dayBox').show().siblings('.taskRateBox').hide();
        break;
      default:
        break;
    }
  });

  // 增量抽取 抽取字段显示
  form.on('radio(addWay)', function(data) {
    console.log(data.value); //被点击的radio的value值
    if (data.value == 'val2') {
      $('.new-zlWaysContent').addClass('active');
    } else {
      $('.new-zlWaysContent').removeClass('active');
    }
  });

  //左侧菜单
  $(document).on('click', '.sidebar-switch', function() {
    if ($('.layui-layout-sjy').hasClass('packup')) {
      $(this).attr('title', '菜单收起');
      $('.layui-layout-sjy').removeClass('packup');
    } else {
      $(this).attr('title', '菜单展开');
      $('.layui-layout-sjy').addClass('packup');
    }
  });

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

  //main-l search-box
  ////选择类型
  $(document).on('click', '.search-box .search-type .cus-select-cont li', function() {
    var type = $(this).attr('sel-type');
    var fa = $(this).parents('.search-box');
    fa.find('.search-cont[sel-cont="' + type + '"]').removeClass('hide').siblings('.search-cont').addClass('hide');
  });
  ////名称输入框
  $('.search-box .search-text .search-text-input').bind('input propertychange', function() {
    var val = $(this).val();
    if (val == '') {
      $(this).parents('.search-text').removeClass('active');
    } else {
      $(this).parents('.search-text').addClass('active');
    }
  });
  $(document).on('click', '.search-box .search-text .search-text-del', function() {
    $(this).siblings('.search-text-input').val('');
    $(this).parents('.search-text').removeClass('active');
  });
  $(document).on('click', '.search-box .search-text .search-text-submit', function() {
    console.log($(this).siblings('.search-text-input').val());
  });
  $(document).on('keyup', '.search-box .search-text .search-text-input', function(e) {
    if (e.keyCode == 13) {
      console.log($(this).val());
    }
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
    if ($('#main_left_tree').hasClass('ztree2')) {
      if (treeNode.level === 1) {
        $('.popout-mainLeftTree').find('.datasubject-menu').removeClass('hide');
      } else {
        $('.popout-mainLeftTree').find('.datasubject-menu').addClass('hide');
      }
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
    var zTree = $.fn.zTree.getZTreeObj(treeId);
    var nodes = zTree.getSelectedNodes()[0];

    zTree.expandNode(treeNode, null, null, null, true);
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

  function mainLeft2BeforeRename(treeId, treeNode, newName, isCancel) {
    if (newName === '') {
      layer.msg('名称不能为空', { icon: 8 });
      $('.main-l-b-tree .newFolder').addClass('disabled');
      var zTree = $.fn.zTree.getZTreeObj(treeId);
      zTree.editName(treeNode);
      return false;
    } else {
      console.log(treeId, treeNode, newName, isCancel);
      $('.main-l-b-tree .newFolder').removeClass('disabled');
    }
  }

  var curExpandNode = null;

  function mainLeft2BeforeExpand(treeId, treeNode) {
    var pNode = curExpandNode ? curExpandNode.getParentNode() : null;
    var treeNodeP = treeNode.parentTId ? treeNode.getParentNode() : null;
    var zTree = $.fn.zTree.getZTreeObj('main_left_tree');
    for (var i = 0, l = !treeNodeP ? 0 : treeNodeP.children.length; i < l; i++) {
      if (treeNode !== treeNodeP.children[i]) {
        zTree.expandNode(treeNodeP.children[i], false);
      }
    }
    while (pNode) {
      if (pNode === treeNode) {
        break;
      }
      pNode = pNode.getParentNode();
    }
    if (!pNode) {
      singlePath(treeNode);
    }
  }

  function singlePath(newNode) {
    if (newNode === curExpandNode) return;

    var zTree = $.fn.zTree.getZTreeObj('main_left_tree'),
      rootNodes, tmpRoot, tmpTId, i, j, n;

    if (!curExpandNode) {
      tmpRoot = newNode;
      while (tmpRoot) {
        tmpTId = tmpRoot.tId;
        tmpRoot = tmpRoot.getParentNode();
      }
      rootNodes = zTree.getNodes();
      for (i = 0, j = rootNodes.length; i < j; i++) {
        n = rootNodes[i];
        if (n.tId != tmpTId) {
          zTree.expandNode(n, false);
        }
      }
    } else if (curExpandNode && curExpandNode.open) {
      if (newNode.parentTId === curExpandNode.parentTId) {
        zTree.expandNode(curExpandNode, false);
      } else {
        var newParents = [];
        while (newNode) {
          newNode = newNode.getParentNode();
          if (newNode === curExpandNode) {
            newParents = null;
            break;
          } else if (newNode) {
            newParents.push(newNode);
          }
        }
        if (newParents != null) {
          var oldNode = curExpandNode;
          var oldParents = [];
          while (oldNode) {
            oldNode = oldNode.getParentNode();
            if (oldNode) {
              oldParents.push(oldNode);
            }
          }
          if (newParents.length > 0) {
            zTree.expandNode(oldParents[Math.abs(oldParents.length - newParents.length) - 1], false);
          } else {
            zTree.expandNode(oldParents[oldParents.length - 1], false);
          }
        }
      }
    }
    curExpandNode = newNode;
  }

  function mainLeft2OnExpand(event, treeId, treeNode) {
    curExpandNode = treeNode;
  }

  function mainLeft2OnClick(event, treeId, treeNode) {
    console.log(event, treeId, treeNode);
  }

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
      beforeRename: mainLeft2BeforeRename,
      beforeExpand: mainLeft2BeforeExpand,
      onExpand: mainLeft2OnExpand,
      onClick: mainLeft2OnClick
    }
  };

  var setting_mainLeft2 = {
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
      beforeRename: mainLeft2BeforeRename,
      beforeExpand: mainLeft2BeforeExpand,
      onExpand: mainLeft2OnExpand,
      onClick: mainLeft2OnClick
    }
  };

  var zNodes_mainLeft1 = [{
    name: '文件夹1',
    children: [{
      iconSkin: 'excel',
      name: 'excel'
    }, {
      iconSkin: 'excel',
      name: 'excel'
    }]
  }, {
    iconSkin: 'excel',
    name: 'excel'
  }, {
    iconSkin: 'txt',
    name: 'txt'
  }, {
    iconSkin: 'hbase',
    name: 'hbase'
  }, {
    iconSkin: 'hive',
    name: 'hive'
  }, {
    iconSkin: 'mongodb',
    name: 'mongodb'
  }, {
    iconSkin: 'mysql',
    name: 'mysql'
  }, {
    iconSkin: 'oracle',
    name: 'oracle'
  }, {
    iconSkin: 'postgresql',
    name: 'postgresql'
  }, {
    iconSkin: 'sqlserver',
    name: 'sqlserver'
  }, {
    iconSkin: 'csv',
    name: 'csv'
  }, {
    iconSkin: 'json',
    name: 'json'
  }, {
    iconSkin: 'json',
    name: 'json'
  }, {
    iconSkin: 'json',
    name: 'json'
  }, {
    iconSkin: 'json',
    name: 'json'
  }, {
    iconSkin: 'json',
    name: 'json'
  }, {
    iconSkin: 'json',
    name: 'json'
  }];

  var zNodes_mainLeft2 = [{
    iconSkin: 'wenjianjia',
    name: '图标都放这里啦',
    children: [{
      iconSkin: 'datasubject',
      name: '数据主题没分享',
      children: [{
        iconSkin: 'dataset',
        name: '数据集没有分享',
      }, {
        iconSkin: 'dataset-share',
        name: '数据集已分享',
      }, {
        iconSkin: 'dataset-edit',
        name: '数据集可编辑',
      }, {
        iconSkin: 'dataset-readonly',
        name: '数据集仅查看',
      }]
    }, {
      iconSkin: 'datasubject-share',
      name: '数据主题已分享',
      children: [{
        iconSkin: 'dataset',
        name: '数据集没有分享',
      }, {
        iconSkin: 'dataset-share',
        name: '数据集已分享',
      }, {
        iconSkin: 'dataset-edit',
        name: '数据集可编辑',
      }, {
        iconSkin: 'dataset-readonly',
        name: '数据集仅查看',
      }]
    }, {
      iconSkin: 'datasubject-edit',
      name: '数据主题可编辑',
      children: [{
        iconSkin: 'dataset',
        name: '数据集没有分享',
      }, {
        iconSkin: 'dataset-share',
        name: '数据集已分享',
      }, {
        iconSkin: 'dataset-edit',
        name: '数据集可编辑',
      }, {
        iconSkin: 'dataset-readonly',
        name: '数据集仅查看',
      }]
    }, {
      iconSkin: 'datasubject-readonly',
      name: '数据主题仅查看',
      children: [{
        iconSkin: 'dataset',
        name: '数据集没有分享',
      }, {
        iconSkin: 'dataset-share',
        name: '数据集已分享',
      }, {
        iconSkin: 'dataset-edit',
        name: '数据集可编辑',
      }, {
        iconSkin: 'dataset-readonly',
        name: '数据集仅查看',
      }]
    }, {
      iconSkin: 'dataset',
      name: '数据集没有分享',
    }, {
      iconSkin: 'dataset-share',
      name: '数据集已分享',
    }, {
      iconSkin: 'dataset-edit',
      name: '数据集可编辑',
    }, {
      iconSkin: 'dataset-readonly',
      name: '数据集仅查看',
    }]
  }, {
    iconSkin: 'wenjianjia',
    name: '文件夹2',
    children: [{
      iconSkin: 'datasubject',
      name: '数据主题2',
      children: [{
        iconSkin: 'dataset',
        name: '数据集2-1',
      }, {
        iconSkin: 'dataset',
        name: '数据集2-2',
      }]
    }, {
      iconSkin: 'datasubject',
      name: '数据主题3',
      children: [{
        iconSkin: 'dataset',
        name: '数据集3-1',
      }, {
        iconSkin: 'dataset',
        name: '数据集3-2',
      }]
    }]
  }];

  if ($('.ztree').hasClass('ztree1')) {
    $.fn.zTree.init($('#main_left_tree'), setting_mainLeft1, zNodes_mainLeft1);
    $.fn.zTree.init($('#main_left_tree_2'), setting_mainLeft1, zNodes_mainLeft1);
  } else if ($('.ztree').hasClass('ztree2')) {
    $.fn.zTree.init($('#main_left_tree'), setting_mainLeft2, zNodes_mainLeft2);
    $.fn.zTree.init($('#main_left_tree_2'), setting_mainLeft2, zNodes_mainLeft2);
  }

  //main-l ztree重命名
  $(document).on('click', '#mainLeftTree_rename', function(e) {
    var zTree = $.fn.zTree.getZTreeObj('main_left_tree');
    var treeNode = zTree.getNodeByTId(mainLeftTree);
    var treeNodeName = treeNode.name;

    zTree.editName(treeNode);
  });

  //main-l ztree删除
  $(document).on('click', '#mainLeftTree_del', function(e) {
    var zTree = $.fn.zTree.getZTreeObj('main_left_tree');
    var treeNode = zTree.getNodeByTId(mainLeftTree);
    if (treeNode.isParent) {
      if (treeNode.children) {
        if (treeNode.children.length > 0) {
          layer.msg('不能删除，请先清空该目录下所有内容', { icon: 8 });
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
      layer.confirm('是否确认删除内容？', {
        btn: ['取消', '确定'],
        btn2: function(index, layero) {
          zTree.removeNode(treeNode);
        }
      });
    }
  });

  function newFolder(treeID, treeType) {
    var zTree = $.fn.zTree.getZTreeObj(treeID);
    if (treeType == 'ztree2') {
      var newNode = {
        iconSkin: 'wenjianjia',
        name: '',
        isParent: true
      };
    } else {
      var newNode = {
        name: '',
        isParent: true
      };
    }

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

      var treeID = _this.parents('.layui-colla-item').find('.ztree').attr('id'),
        treeType = _this.parents('.layui-colla-item').find('.ztree').hasClass('ztree1') ? 'ztree1' : 'ztree2';
      newFolder(treeID, treeType);
    }
    e.stopPropagation();
  });

  //main-l-b-tree点击标题
  $('.main-l-b-tree .title-name').click(function(e) {
    e.stopPropagation();
    console.log('全部');
  });

  //新建数据连接
  $(document).on('click', '.pop-addDataConnection', function(e) {
    $('.pop-cont-addDataConnection').removeClass('hide');
    layer.open({
      type: 1,
      title: '新建数据连接',
      area: ['660px', 'auto'], //宽高
      content: $('.pop-cont-addDataConnection'),
      end: function(index1, layero1) {
        $('.pop-cont-addDataConnection').addClass('hide');
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
  $(document).on('click', '.cus-menulist dt .tit', function() {
    var fa = $(this).parents('dl').eq(0);
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
  });

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
    var fa = $(this).parents('.list');
    fa.find('li').removeClass('active');
    $(this).addClass('active');
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
  // laydate.render({
  //   elem: '#startDate' //指定元素
  // });
  // // 结束日期
  // laydate.render({
  //   elem: '#endDate' //指定元素
  // });
  lay('.startDate').each(function() {
    laydate.render({
      elem: this,
      trigger: 'click'
    });
  });
  lay('.endDate').each(function() {
    laydate.render({
      elem: this,
      trigger: 'click'
    });
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

      },
      end: function(index1, layero1) {
        $('.pop-cont-details').addClass('hide');
      },
    });
  }

  //修改分类
  $(document).on('click', '.pop-addToCategory', function() {
    $('.pop-cont-addToCategory').removeClass('hide');
    var addToCategory = layer.open({
      type: 1,
      skin: 'layer-over',
      area: ['440px', 'auto'],
      title: '修改分类',
      content: $('.pop-cont-addToCategory'),
      btnAlign: 'c',
      btn: ['取消', '确定'],
      end: function() {
        $('.pop-cont-addToCategory').addClass('hide');
      }
    });
  });

  //修改密码弹窗
  $(document).on('click', '.pop-editPassword', function() {
    $('.pop-cont-editPassword').removeClass('hide');
    var editPassword = layer.open({
      type: 1,
      scrollbar: false,
      area: ['560px', 'auto'],
      title: '修改密码',
      content: $('.pop-cont-editPassword'),
      btnAlign: 'c',
      btn: ['取消', '确定'],
      btn2: function(index, layero) {
        var oldpwd = layero.find('input[name="oldpwd"]'),
          newpwd = layero.find('input[name="newpwd"]'),
          newpwd2 = layero.find('input[name="newpwd2"]'),
          rule = /^.{8,16}$/;
        if ($.trim(oldpwd.val()).length <= 0) {
          oldpwd.addClass('error');
          oldpwd.parent('.layui-input-block').siblings('.form-item-tips').addClass('fc-red').text('原始密码不正确');
        } else {
          oldpwd.removeClass('error');
          oldpwd.parent('.layui-input-block').siblings('.form-item-tips').addClass('fc-red').text('');
          if (!rule.test($.trim(newpwd.val()))) {
            newpwd.addClass('error');
            newpwd.parent('.layui-input-block').siblings('.form-item-tips').addClass('fc-red');
          } else {
            newpwd.removeClass('error');
            newpwd.parent('.layui-input-block').siblings('.form-item-tips').removeClass('fc-red');
            if ($.trim(newpwd2.val()) !== $.trim(newpwd.val())) {
              newpwd2.addClass('error');
              newpwd2.parent('.layui-input-block').siblings('.form-item-tips').addClass('fc-red').text('新密码输入不一致');
            } else {
              newpwd2.removeClass('error');
              newpwd2.parent('.layui-input-block').siblings('.form-item-tips').addClass('fc-red').text('');
              layer.close(index);
              layer.msg('修改密码成功', { icon: 7 });
            }
          }
        }
        return false;
      },
      end: function() {
        $('.pop-cont-editPassword').addClass('hide');
      }
    });
  });


  exports('index', {});

});
