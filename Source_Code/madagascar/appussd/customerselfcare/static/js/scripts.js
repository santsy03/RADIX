var showMessages = function(err, ok) { 
    $("#errmsg").remove();
    $("#okmsg").remove();    
    if (err != '') { 
        $("#messages").append("<div id='errmsg' class='errmsg'></div>"); 
        $("#errmsg").append(err); 
        }
    if (ok != '') { 
        $("#messages").append("<div id='okmsg' class='okmsg'></div>"); 
        $("#okmsg").append(ok); 
        }
}

var showLoading = function() {
	$("#loading")
		.css({visibility:"visible"})
		.css({opacity:"1"})
		//.css({display:"block"})
}

var hideLoading = function() { $("#loading").fadeTo(1000, 0); };

var goBackToParent = function(url) { window.location.href = url; } 

function goBackToHome() { window.parent.location.href = '/'; }

function IsNumeric(input) {
    return (input - 0) == input && input.length > 0;
}
$(document).ready(function(){
    $('#containerforlinks ul li a').click(function(ev){
    $('#containerforlinks ul li').removeClass('selected');
    $(ev.currentTarget).parent('li').addClass('selected');
    });
    $("#me2uhistory").click(function(e) {
        //$("#errmsg").remove();
        e.preventDefault();
        var subscriberno = $("#subscriberno").val();
        var obj = $.cookie("sessionid",  { path: '/', secure: true});
        var csrftoken = $.cookie('csrftoken');
        //$("#mymsg").html(obj);
        if (subscriberno == '') {
            $("#errmsg").html('Please enter a subscriber number.');
            return false;
        }
        if (subscriberno.length < 9) {
            $("#errmsg").html('Please enter a valid subscriber number.');
            return false;
        }
        //$.colorbox({href:"/me2udata/"});
        $("#errmsg").html("<img src='/static/images/ajax-loader.gif'/>");
        $.ajax({
    	    type: "POST",
    	    crossDomain: false,
    	    data: {'msisdn': subscriberno, 'action': 2, 'csrfmiddlewaretoken': csrftoken },
    	    dataType: "json",
    	    url: "/me2u/",
    	    success: function(data){
	        if (data.length == 0) {
    		    $('#errmsg').html("No data for "+subscriberno);
    		}else{
    		     //$('#errmsg').html(data);
    		     content = "<table width='100%' class='datagrid'>"
    		     content += "<th>Recipient</td>";
    		     content += "<th>Amount</td>";
    		     content += "<th>Status</td>";
    		     content += "<th>Transaction Date / Time</td>";
    		     $.each(data, function(key, val) {
    		         content += "<tr>"
    			 content += "<td class='{% cycle 'odd' 'even' %}'>" + data[key].recipient + "</td>";
    			 content += "<td class='{% cycle 'odd' 'even' %}'>" + data[key].amount + "</td>";
    			 content += "<td class='{% cycle 'odd' 'even' %}'>" + data[key].status + "</td>";
    			 content += "<td class='{% cycle 'odd' 'even' %}'>" + data[key].created_at + "</td>";
    			 content += "</tr>";
    		     });
                 var dlink = '<a href="/me2u/export/'+subscriberno+'">Export Data</a>';
    		     var title = "Me2u History data for " + subscriberno +" | "+ dlink;
    		     $.colorbox({html:content+"</table>", title:title, width:"90%", height:"85%"});
    		     $("#errmsg").empty();
    		}
    	    },
    	    error: function(e){
    	        $("#errmsg").html('Please refresh page and try again'+e);
    	}
    	});
    });

    $("#me2uform").submit(function(e) {
        e.preventDefault();
        var subscriberno = $("#subscriberno").val();
        var csrftoken = $.cookie('csrftoken');
        var values = {'msisdn': subscriberno, 'action': 1,
                      'csrfmiddlewaretoken': csrftoken };
        $("#cresults").empty();
        $("#errmsg").empty().css({border: "0px", padding: "0px"});
        if (!IsNumeric(subscriberno)) {
            $("#messages").html('The MSISDN should be numbers only.');
            return false;
        }
        if (subscriberno.length < 9) {
            $("#messages").html('Please enter a valid subscriber number.');
            return false;
        }
        $("#messages").html("<img src='/includes/images/ajax-loader.gif'/>");
        $.ajax({
            type: "POST",
            data: values,
            dataType: "json",
            url: "/me2u/",
            success: function(data){
                var code = data.code;
                var pin = data.pin;
                var last_trans = data.last_trans;
                if (last_trans.length == 0){
                    nodata = '<div class="note">No Me2u history data found.</div>';
                    $("#me2usum").html(nodata);
                }else{
                    $("#me2uhistory").css({display:"inline-block"});
                    var ltrans = last_trans[0];
                    me2udata = "<div class='label'>Recipient:</div><div class='data'>" + ltrans.recipient;
                    me2udata += "</div><div class='label'>Amount:</div><div class='data'>" + ltrans.amount;
                    me2udata += "</div><div class='label'>Status:</div><div class='data'>" + ltrans.status;
                    me2udata += "</div><div class='label'>Date:</div><div class='data'>" + ltrans.created_at;
                    me2udata += "</div>";
                    $("#me2usum").html(me2udata);
                }
                $("#messages").html("Operation Successful");
                $("#id_active").html(data.active);
                $("#id_wdate").html(data.date);
                $("#id_pinstatus").html(data.pin_status);
                if (code == 1){
                    $("#btnwhitelist").hide();
                    if (pin == 1){
                        $("#btnunlock").hide();
                        $("#btnreset").css({display:"inline-block"});
                    }else{
                         $("#btnunlock").css({display:"inline-block"});
                         $("#btnreset").css({display:"inline-block"});
                    }
                }else{
                    $("#btnreset").hide();
                    $("#btnunlock").hide();
                    $("#btnwhitelist").css({display:"inline-block"});
                }
                $("#id_info").css({display: "block"});
            },
            error: function(){
                $("#messages").html('Error occured while checking Me2u status.');
            }
        });
    });
    $('#fupload').html('<input id="msisdns" name="msisdns" type="file" />');
    $("#btnme2ubulk").colorbox({inline:true, width:"55%", height:"50%", href:"#me2u_bulk"});
    
    $("#uploadwlist").submit(function(e) {   
        $("#results").empty();
        e.preventDefault();
        var formData = new FormData($('#uploadwlist')[0]);
        $("#results").html("<img src='/includes/images/ajax-loader.gif'/>");
        $.ajax({
            type: "POST",
            crossDomain: false,
            enctype: 'multipart/form-data',
            data: formData,
            //Options to tell jQuery not to process data or worry about content-type.
            cache: false,
            contentType: false,
            processData: false,
            url: "/whitelist/bulk/",
            success: function(data){
                $('#results').html(data.message);
            },
            error: function(e){
                $("#results").html('Please refresh page and try again'+e);
        }
        });
    });
    $("#btnwhitelist").click(function(e) {
        e.preventDefault();
        var subscriberno = $("#subscriberno").val();
        var csrftoken = $.cookie('csrftoken');
        if (subscriberno == '') {
            $("#errmsg").html('Balance check available ONLY for activated packages.');
            return false;
        }
        $("#errmsg").html("<img src='/static/images/loading.gif'/>");
        $.ajax({
            type: "POST",
            data: {'msisdn': subscriberno, 'action': 2, 'csrfmiddlewaretoken': csrftoken },
            dataType: "json",
            url: "/whitelist/do/",
            success: function(data){
                    $("#messages").html(data.message);
                    if (data.status == 4){
                        $("#id_active").html('Yes');
                    }
                    $("#errmsg").empty();               
            },
            error: function(e){
                $("#messages").html('Please refresh page and try again' + e);
                $("#errmsg").empty();
        }
        });
    });
    $("#btnunlock").click(function(e) {
        e.preventDefault();
        var subscriberno = $("#subscriberno").val();
        var csrftoken = $.cookie('csrftoken');
        if (subscriberno == '') {
            $("#errmsg").html('Balance check available ONLY for activated packages.');
            return false;
        }
        $("#errmsg").html("<img src='/static/images/loading.gif'/>");
        $.ajax({
            type: "POST",
            data: {'msisdn': subscriberno, 'action': 3, 'csrfmiddlewaretoken': csrftoken },
            dataType: "json",
            url: "/me2u/",
            success: function(data){
                    $("#messages").html(data.message);
                    $("#errmsg").empty();               
            },
            error: function(e){
                $("#messages").html('Please refresh page and try again' + e);
                $("#errmsg").empty();
        }
        });
    });
    $("#btnreset").click(function(e) {
        e.preventDefault();
        var subscriberno = $("#subscriberno").val();
        var csrftoken = $.cookie('csrftoken');
        if (subscriberno == '') {
            $("#errmsg").html('Balance check available ONLY for activated packages.');
            return false;
        }
        $("#errmsg").html("<img src='/static/images/loading.gif'/>");
        $.ajax({
            type: "POST",
            data: {'msisdn': subscriberno, 'action': 4, 'csrfmiddlewaretoken': csrftoken },
            dataType: "json",
            url: "/me2u/",
            success: function(data){
                    $("#messages").html(data.message);
                    $("#errmsg").empty();               
            },
            error: function(e){
                $("#messages").html('Please refresh page and try again' + e);
                $("#errmsg").empty();
        }
        });
    });
});
