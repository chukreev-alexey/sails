function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$(document).ready(function() {
    $.ajaxSetup({
    //    cache: false,
    //    type: 'POST',
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });
    $(".ConfirmPay").live('click', function(){
        if (!confirm('Вы уверены?')) {
            return false;
        }
        var obj = $(this);
        if (!obj.attr('pid')) {
            return false;
        }
        $.ajax({
            url: '/confirm/payments/'+obj.attr('pid')+'/',
            type: "POST",
            dataType: 'html',
            success: function (html) {
                obj.parents(".ManagerChecker:eq(0)").html(html);
            },
            error: function () {
                //$("#HideBlock").hide();
                alert("Ошибка при подтверждении платежа.");
            }
        });
        return false;
    });
});