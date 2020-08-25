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

layui.define(['element', 'layer'], function(exports) {

    var $ = layui.jquery,
        element = layui.element,
        layer = layui.layer;

    (function($) { //模拟下拉选择框
        var selection = function(element) {
            this.$element = $(element).closest('.sel-model');
            var _this = this;
            this.$element.on('click', function(event) {
                event.stopPropagation();
            });
            this.$element.on('click', '.model-txt,.model-icon', function() {
                var fa = $(this).parents('.sel-model');
                if (fa.hasClass('selected')) {
                    fa.addClass('selected');
                    _this.hide();
                } else {
                    $('.sel-model').removeClass('selected');
                    _this.show();
                }
            });
            this.$element.on('click', '.model-txt span i', function(event) {
                event.stopPropagation();
                var dom = $(this).parent();
                var name = dom.attr('class');
                dom.remove();
                _this.$element.find('.model-list li[name="' + name + '"]').removeClass('active');
            });
            this.$element.on('click', '.model-list li', function(event) {
                event.stopPropagation();
                var txt = $(this).children('a').text();
                var name = $(this).attr('name');
                if ($(this).hasClass('active')) {
                    $(this).removeClass('active');
                    _this.$element.find('.model-txt').find('.' + name).remove();
                } else {
                    if (name == 'all') {
                        _this.$element.find('.model-txtbox').find('span').remove();
                        _this.$element.find('.model-list li').each(function() {
                            if ($(this).attr('name') != 'all' && $(this).attr('name') != 'clean') {

                                $(this).addClass('active');
                                var txt = $(this).children('a').text();
                                var name = $(this).attr('name');
                                _this.$element.find('.model-txtbox').append('<span class=' + name + '>' + txt + '<i class="icon-sjjm-cuo"></i></span>');
                            }
                        });
                    } else if (name == 'clean') {
                        _this.$element.find('.model-txtbox').find('span').remove();
                        _this.$element.find('.model-list li').removeClass('active');
                    } else {
                        $(this).addClass('active');
                        _this.$element.find('.model-txtbox').append('<span class=' + name + '>' + txt + '<i class="icon-sjjm-cuo"></i></span>');
                    }
                }
            });
            this.$element.on('click', '.model-del', function() {
                _this.$element.find('.model-txtbox').find('span').remove();
                _this.$element.find('.model-list li').removeClass('active');
            });
        };
        selection.prototype.show = function() {
            this.$element.addClass('selected');
        };
        selection.prototype.hide = function() {
            this.$element.removeClass('selected');
        };
        var PlugIn = function() {
            return this.each(function() {
                var $this = $(this);
                var data = $this.data('selection');
                if (!data) {
                    $this.data('selection', (data = new selection(this)));
                }
            });
        };

        $.fn.selection = PlugIn;

    })(jQuery);

    $('.sel-model').selection();

    //左侧菜单
    $(document).on('click', '.sidebar-switch a', function() {
        var _this = $(this);
        if ($('.layui-layout-sjjm').hasClass('packup')) {
            $('.layui-layout-sjjm').removeClass('packup');
            _this.attr('title', '菜单收起').html('<i class="icon icon-sjjm-shouqicaidan"></i>');
        } else {
            $('.layui-layout-sjjm').addClass('packup');
            _this.attr('title', '菜单展开').html('<i class="icon icon-sjjm-zhankaicaidan"></i>');
        }
    });

    //自定义select
    $(document).on('click', '.cus-select .cus-select-btn', function() {
        var _this = $(this);
        var fa = _this.parents('.cus-select');
        if (fa.hasClass('cus-selected')) {
            fa.removeClass('cus-selected');
        } else {
            fa.addClass('cus-selected');
        }
        $('.layui-form-select').removeClass('layui-form-selected');
    });
    $(document).on('click', '.cus-select,.proFolderAdd,.sel-model .model-list', function(e) {
        e.stopPropagation();
    });
    $(document).on('click', function(e) {
        if (e.which == 1) {
            $('.cus-select').removeClass('cus-selected');
            $('.popout-btn').removeClass('active');
            $('.popout-box').removeClass('active');
            $('.sel-model').removeClass('selected');
        }
    });

    //scroll
    $('.scroll,.main-l-b').niceScroll(niceScroll_option);
    $(document).on('mouseenter touchstart', '.scroll,.main-l-b,.main-r,.modeling-cont', function() {
        if ($(this).getNiceScroll == undefined || $(this).getNiceScroll().length == 0) {
            scroll();
        }
    });

    exports('common', {});
});
