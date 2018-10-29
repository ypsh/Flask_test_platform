function upperCase(id) {
    var phone = document.getElementById(id).value;
    if (phone != '') {
        if (!(/^1[34578]\d{9}$/.test(phone))) {
            toastr.info("手机号码有误，请重填");
            return false;
        }
    }

}

function submit(elementid) {
    $('#submit').bind('click', function () {
        $.getJSON($SCRIPT_ROOT + '/_add_numbers', {
            elementid: $('input[name=elementid]').val(),
        }, function (data) {
            $("#result").text(data.result);
        });
        return false;
    });
}

function submit_loansucess() {
    $('#submit04.btn').button('loading')
    $.post("/apis/loansuccess", {
        mobile: $('#mobilenumber04').val(),
        product: $('#product04').val()
    }, function (data, status) {
        $('#body04').val(JSON.stringify(data.body, null, 4));
        $('#result04').val(JSON.stringify(data.result, null, 4));
        $('#submit04.btn').button('reset');
    }).error(function () {
        $('#submit01.btn').button('reset');
        toastr.info('获取失败：');
    })
}
function submit_credit() {
    $('#submit01.btn').button('loading')
    $.post("/apis/credit", {
        mobile: $('#mobilenumber01').val(),
        product: $('#product01').val()
    }, function (data, status) {
        $('#body01').val(JSON.stringify(data.body, null, 4));
        $('#result01').val(JSON.stringify(data.result, null, 4));
        $('#submit01.btn').button('reset');
    }).error(function () {
        $('#submit01.btn').button('reset');
        toastr.info('获取失败：');
    })
}
function submit_message() {
    $('#submit.btn').button('loading')
    $.post("/apis/message", {
        mobile: $('#mobilenumber').val(),
    }, function (data, status) {
        $('#result').val(JSON.stringify(data, null, 4));
        $('#submit.btn').button('reset');
    }).error(function () {
        $('#submit.btn').button('reset');
        toastr.info('获取失败：');
    })
}

function submit_aes() {
    $('#submit.btn').button('loading')
    $.post("/apis/aes", {
        aes: $('#inputtext').val(),
    }, function (data, status) {
        $('#result').val(JSON.stringify(data, null, 4));
        $('#submit.btn').button('reset');
    }).error(function () {
        $('#submit.btn').button('reset');
        toastr.info('获取失败：');
    })
}

function submit_oa() {
    $('#submit02.btn').button('loading')
    $.post("/apis/oa", {
        mobile: $('#mobilenumber02').val(),
        amount: $('#amount').val(),
        status: $('#status').val(),
    }, function (data, status) {
        $('#body02').val(JSON.stringify(data.body, null, 4));
        $('#result02').val(JSON.stringify(data.result, null, 4));
        $('#submit02.btn').button('reset');
    }).error(function () {
        $('#submit02.btn').button('reset');
        toastr.info('获取失败：');
    })
}

function submit_ob() {
    $('#submit03.btn').button('loading')
    $.post("/apis/ob", {
        mobile: $('#mobilenumber03').val(),
        status: $('#status02').val(),
    }, function (data, status) {
        $('#body03').val(JSON.stringify(data.body, null, 4));
        $('#result03').val(JSON.stringify(data.result, null, 4));
        $('#submit03.btn').button('reset');
    }).error(function () {
        $('#submit03.btn').button('reset');
        toastr.info('获取失败：');
    })
}

function getheml() {
    $.get('/admin',
        function (data, status) {
            toastr.info("数据：" + data + "\n状态：" + status);

        })
}

//检查用户登录状态
function checkup() {
    var username = ''
    var token = ''
    username = localStorage.user
    token = localStorage.token
    $.get("/apis/user", {
        username: username,
        token: token,
    }, function (data, status) {
        if (data != null && data.status == false) {
            window.location.href = "/login"
        }
    }).error(function () {
        toastr.info('获取失败：');
    })
}
//登出
function logout() {
    localStorage.clear()
    window.location.href = "/login"
}
//添加模拟服务
var operate = 'add';
function add_service() {
    $('#submit.btn').button('loading')
    $.post("/apis/service", {
        service_name: $('#service_name').val(),
        service_type: $('#service_type').val(),
        status: $("input[type='radio']:checked").val(),
        data: $('#data').val(),
        user: localStorage.user,
        operate: operate,
    }, function (data, status) {
        if (data != null && data.message == true) {
            $('#submit.btn').button('reset');
            table.ajax.reload()
            toastr.info('操作成功');
        } else {
            toastr.info(operate + data.message);
            $('#submit.btn').button('reset');
        }
    }).error(function () {
        $('#submit.btn').button('reset');
        toastr.error('操作失败');
    })
}

function formate_json(id) {
    var textarea = document.getElementById(id);
    var textarea_value = textarea.value;
    textarea.value = (JSON.stringify(JSON.parse(textarea.value), null, 4));
}
//添加更新api
var operate = 'add';
function add_apimanger() {
    $('#submit.btn').button('loading')
    $.post("/apis/apimanager", {
        api_name: $('#service_name').val(),
        model: $('#model').val(),
        type: $('#service_type').val(),
        path: $('#path').val(),
        headers: $('#header').val(),
        need_token: $("input[name='token']:checked").val(),
        status: $("input[name='status']:checked").val(),
        mark: $('#remake').val(),
        user: localStorage.user,
        operate: operate,
    }, function (data, status) {
        if (data != null && data.message == true) {
            $('#submit.btn').button('reset');
            table.ajax.reload()
            toastr.info('操作成功');
        } else {
            toastr.info(operate + data.message);
            $('#submit.btn').button('reset');
        }
    }).error(function () {
        $('#submit.btn').button('reset');
        toastr.error('操作失败');
    })
}
//获取API清单
function get_service_list() {
    $.get('/apis/apimanager',
        function (data, status) {
            if (data.data.length > 0) {
                for (var i = 0; i < data.data.length; i++) {
                    $('#service_data')
                        .append('<option label="' + data.data[i][1] + '" value="' + data.data[i][1] + '"></option>');
                }
            }
        }

    )
}
//获取模块清单
function get_model_list(id) {
    $.get('/apis/modelist',
        function (data, status) {
            if (data.data.length > 0) {
                for (var i = 0; i < data.data.length; i++) {
                    $('#' + id)
                        .append('<option label="' + data.data[i] + '" value="' + data.data[i] + '"></option>');
                }
            }
        }

    )
}



function is_selected(table) {
    if (operate === 'update') {
        if (table.rows(['.selected'])[0] != "") {
            case_id = table.rows(['.selected']).data()[0][1]
        } else {
            toastr.error('请选择数据');
        }

    } else {
        case_id = ''
    }

}
//判断是否选中行
function selected(table) {
    if (table.rows(['.selected'])[0] != "") {
        return true
    } else {
        return false
    }

}


Date.prototype.format = function (format) {
    var o = {
        "M+": this.getMonth() + 1, //month
        "d+": this.getDate(),    //day
        "h+": this.getHours(),   //hour
        "m+": this.getMinutes(), //minute
        "s+": this.getSeconds(), //second
        "q+": Math.floor((this.getMonth() + 3) / 3),  //quarter
        "S": this.getMilliseconds() //millisecond
    }
    if (/(y+)/.test(format)) format = format.replace(RegExp.$1,
        (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o) if (new RegExp("(" + k + ")").test(format))
        format = format.replace(RegExp.$1,
            RegExp.$1.length == 1 ? o[k] :
                ("00" + o[k]).substr(("" + o[k]).length));
    return format;
}

function clearval(id) {
    $('#' + id).val('')
}