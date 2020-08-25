/**
 * 成功后刷新
 * @param msg 提示
 */
function okAction(msg) {
    layer.msg(msg, {
        icon: 7
    });
    setTimeout(function () {
        //loadTree();
        window.location.reload(true)
        layer.closeAll();
    }, 1500);
}

function okActionReport(msg, url) {
    layer.msg(msg, {
        icon: 7
    });
    setTimeout(function () {
        window.location.href = ctx + url;
        layer.closeAll();
    }, 1500);
}

function pop_succeed(mag) {
    return layer.msg(mag, {
        icon: 7
    });
}

function pop_failure(mag) {
    return layer.msg(mag, {
        icon: 8
    });
}

function pop_info(mag) {
    return layer.msg(mag, {
        icon: 9
    });
}

function pop_network(mag) {
    return layer.msg(mag, {
        icon: 10
    });
}

function pop_running(mag) {
    mag = mag || "加载中...";
    return layer.msg(mag, {
        icon: 11,
        shade: true,
        time: 0
    });
}