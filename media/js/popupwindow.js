function ClosePopup(){
	$("#HideBlock, #PopupWindow").hide();
	$("#PopupWindow").hide();
	return false;
}

function ShowPopup(url) {
	var obj = $(this);
	if (obj.attr('href')) {
		url = obj.attr('href');
	}
	if (!url) {
		return false;
	}
	$("#HideBlock").show();
	$(document).keyup(function(e) { //test this
		if (e.keyCode == 27) { ClosePopup(); } // close popup on esc
	});
	$("html").click(function(e) {
		ClosePopup();
	});
	$('.Popup').click(function(event) {
		event.stopPropagation();
	});
	$.ajax({
		url: url,
		type: "GET",
		dataType: 'html',
		error: function () {
			$("#HideBlock").hide();
		},
		success: function (html) {
			$("#PopupContent").html(html);
			$("#PopupWindow form").submit(SubmitForm);
			$("#PopupWindow").show();
		}
	});
	return false;
}

function SubmitForm(){
	if ($(this).hasClass("NotClickable")) {
		return false;
	}
    if ($(this).hasClass('FormPayments')) {
        if (!confirm('Вы уверены, что хотите добавить платеж?')) {
            return false;
        }
    }
	var form = $(this);
	form.addClass("NotClickable");
	data = form.serializeArray();
	$.ajax({
		url: form.attr('action'),
		type: "POST",
		dataType: 'json',
		data: data,
		error: function () {
			form.removeClass("NotClickable");
			alert("Ошибочка закралась.");
		},
		success: function (data) {
			form.removeClass("NotClickable");
			form.find('span.errors').remove();
			if (data && data.errors) {
                $("ul.messages").detach();
				for (var item in data.errors) {
					tag = '<span class="errors">' + data.errors[item] + '</span>';
					if (item == 'captcha') {
						item = 'captcha_0';
					}
					form.find("#id_" + item).parent().parent().find(".FormError").append(tag);
				}
				form.find("a[href=#refresh]").click();
				return false;
			}
			else {
				ShowPopup(form.attr('action'));
			}
		}
	});
	return false;
}
$(document).ready(function() {
	//$("#ClosePopup").live('click', ClosePopup);
	$("#ClosePopup").click(ClosePopup);
	$(".AddPayment").live('click', ShowPopup);
    
    /* Редактирование комментариев */
    $("#PopupContent").on("click", "a.EditComment", function(){
        var $parent = $(this).closest(".Comments");
        $parent.find(".NotEditableComment").hide();
        $parent.find(".EditableComment").show();
        return false;
    });
    $("#PopupContent").on("click", ".ButtonCancelCommentChange", function(){
        var $parent = $(this).closest(".Comments");
        $parent.find(".NotEditableComment").show();
        $parent.find(".EditableComment").hide();
        return false;
    });
    $("#PopupContent").on("click", ".ButtonSaveComment", function(){
        var payment_id = parseInt($(this).closest(".GridRow[item_id]").attr('item_id')),
            $parent = $(this).closest(".Comments"),
            comment = $parent.find(".EditableComment textarea[name=comment]").val();
            order_url = $("form.FormPayments").attr('action');
        if (!payment_id) return false;
        
        $.ajax({
            url: URL_CHANGE_PAYMENT_COMMENT,
            type: "POST",
            data: {payment: payment_id, comment: comment},
            success: function (html) {
                ShowPopup(order_url);
            },
            error: function () {
                alert("Во время сохранения комментария произошла ошибка.");
            }
        });
        
        $parent.find(".NotEditableComment").show();
        $parent.find(".EditableComment").hide();
        return false;
    });
    
});