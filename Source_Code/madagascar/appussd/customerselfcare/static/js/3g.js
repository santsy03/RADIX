function loadPackages() {
    $.ajax({
        type: 'GET',
        url: '/json/packages',
        dataType: 'json',
        success: function(json) {
            $('#id_bundles').empty();
            //$('#id_flashbundles').empty();
            //$('#id_devicebundles').empty();
            $.each(json, function(i, record) {
                $('#id_bundles').append($("<option></option>").attr("value", record.pk)
            	.text(record.fields.package_name + ' - MGA ' + (record.fields.package_cost )));
            });
        },
        error: function(err) {
        	//alert("Error Loading Package List");
        	$("#messages").html("Error Loading Package List" + err.Message);
        }
    });
}

function IsNumeric(input) {
    return (input - 0) == input && input.length > 0;
}

$(document).ready(function() {
    //loadPackages();
    $("#searchform").submit(function(e) {
        $("#errmsg").remove();
        $("#okmsg").remove();
        $("#id_subscriberno").html('-');
        $("#id_prepaid").html('-');
        $("#id_balance").html('-');
        $("#tableholder").html('');
        e.preventDefault();
        $("#progress").css({display: "block"});
        $("#messages").removeClass( "alert alert-success" );
        $("#messages").removeClass( "alert alert-error" );
        var subscriberno = $("#subscriberno").val();
        if (subscriberno == 'Search...') {
            showMessages('Please enter a subscriber number.', '');
            return false;
        }
        if (!IsNumeric(subscriberno)) {
            showMessages('The subscriber number should be numbers only.', '');
            return false;
        }
        if (subscriberno.length < 9) {
            showMessages('Please enter a valid subscriber number.', '');
            return false;
        }
        var csrftoken = $.cookie('csrftoken');
        var data = {};
        data["subscriberno"] = subscriberno;
        data["csrfmiddlewaretoken"] = csrftoken;
        data["subscribetoservice"] = '';

    	$.ajax({
    		type: "POST",
    		data: data,
    		dataType: "json",
    		url: "/3g/",
    		success: function(data){
    			$('#id_subscriberno').html(subscriberno);
    			$('#id_prepaid').html(data.prepaid);
    			$('#id_balance').html(data.balance);
    			var serviceplans = data.serviceplans;
    			table_head = "<table id='tableitems' class='services'>";
    			table_head += "<tr class='head'><td class='head'>Package</td><td class='head'>Active</td>";
    			table_head += "<td class='head'>Subscription Date</td>";
                        table_head += "<td class='head'>Fee Charged</td>";
    			table_head += "<td class='head'>Expiry Date</td><td class='head'>Balance</td></tr>";
    			var table_header = table_head;
    			var table_footer = "</table>";
    			var active_status = "";
    			var content = '';
    			$.each(serviceplans, function(key, val) {
			    content += "<tr class='lists'><td class='{% cycle 'odd' 'even' %}'>" + serviceplans[key].serviceplan + "</td>";
			    content += "<td class='{% cycle 'odd' 'even' %}'>" + serviceplans[key].active + "</td>";
			    content += "<td class='{% cycle 'odd' 'even' %}'>" + serviceplans[key].subdate + "</td>";
                            content += "<td class='{% cycle 'odd' 'even' %}'>" + serviceplans[key].fee + "</td>";
			    content += "<td class='{% cycle 'odd' 'even' %}'>" + serviceplans[key].expirydate + "</td>";
			    content += "<td class='{% cycle 'odd' 'even' %}'> " + serviceplans[key].balance + " </td></tr>";
    			});
                $("#id_info").css({display: "block"});
                $("#id_trans").css({display:"inline-block"});
                $("#tableholder").html(table_header + content + table_footer);
                $("#btnadd").css({display: "block"});
                $("#btnhistory").css({display: "block"});
                $("#btnrenewhistory").css({display: "block"});
                $("#btnrenewstop").css({display: "block"});
    		    $("#messages").empty();
                $("#progress").empty();
    		},
    		error: function(){
    		//alert("Error occrured while fetching subscriber details.");
    		$("#messages").html('Please refresh page and try again').css({color:'#ff0000'});
            $("#messages").addClass( "alert alert-error" );
            $("#progress").empty();
    		}
    	});
    });

    $("#btnrenewstop").click(function() {		
	var subscriberno = $('#subscriberno').val();
    var csrftoken = $.cookie('csrftoken');
    $("#messages").removeClass( "alert alert-success" );
    $("#messages").removeClass( "alert alert-error" );
	var values = {'msisdn': subscriberno, 
                      'action': 'stop',
                      'package': 'Stop renewal - MGA 0',
                      'csrfmiddlewaretoken': csrftoken,
                      'packageID': 0, 'auto': 0};
	$.ajax({
	    type: "POST",
	    data: values,
	    dataType: "text",
	    url: "/provision/",
	    success: function(data){
	        $("#messages").html(data);
            $("#messages").addClass( "alert alert-success" );
		},
		error: function(){
		    $("#messages").html('There was an error processing request try again').css({color:'#ff0000'});
            $("#messages").addClass( "alert alert-error" );
		    }
		});
	});
});


function addSubscription() {
    var subscriberno = $('#subscriberno').val();
    var packageId = 0;
    var service = $("#id_service").val();
    var auto_renew = $("#id_autorenew").val();
    var pack_details = $("#id_bundles option:selected").text();
    $("#messages").removeClass( "alert alert-success" );
    $("#messages").removeClass( "alert alert-error" );
    if (service == '') {
        showServiceMessages('Please select a 3G service.', '');
        return false;
    }
    if (service == '1') {
        //bundles
    	var bundles = $("#id_bundles").val();
        if (bundles == '') {
            showServiceMessages('Please select an internet bundle.', '');
            return false;
        }
        packageId = bundles;
    }
    if (service == '2') {
        //Flash bundles
    	var flash = $("#id_flashbundles").val();
        //$("#id_bundles").prop("disabled", true);
        if (flash == '') {
            showServiceMessages('Please select a flash bundle.', '');
            return false;
        }
        packageId = flash;
    }
    if (service == '3') {
        //Device bundles
        var device = $("#id_devicebundles").val();
        if (device == '') {
            showServiceMessages('Please select a device bundle.', '');
            return false;
        }
        packageId = device;
    }
    var csrftoken = $.cookie('csrftoken');	
    var values = {'msisdn': subscriberno, 
                  'packageID': packageId,
                  'package': pack_details,
                  'csrfmiddlewaretoken': csrftoken,
                  'auto': auto_renew, 'action': 'False'};
    $("#messages").html("<img src='/static/images/loading.gif'/>");
    $.ajax({
    	type: "POST",
    	data: values,
    	dataType: "text",
    	url: "/provision/",
    	success: function(data){
    		//alert(data);
    		$("#messages").html(data);
            $("#messages").addClass( "alert alert-success" );
    	},
    	error: function(){
    		//alert("Error occured while making provisioning request");
    		$("#messages").html('Error occured while making provisioning request.');
            $("#messages").addClass( "alert alert-error" );
    	}
    });
    $.colorbox.close();
    //$('#fade , .popup_block').fadeOut(function() {
    //     $('#fade, a.close').remove();
    //});
}

var showServiceMessages = function(err, ok) {
    $("#errmsg").remove();
    $("#okmsg").remove();
    if (err != '') {
        $("#servicemessages").append("<div id='errmsg' class='errmsg'></div>");
        $("#errmsg").append(err);
    }
    if (ok != '') {
        $("#servicemessages").append("<div id='okmsg' class='okmsg'></div>");
        $("#okmsg").append(ok);
    }
}

$(document).ready(function() {
    var my_sess = $.cookie("sessionid",  { path: '/'});
    $('#btnhistory').click(function() {
        var subscriberno = $('#subscriberno').val();
        //window.location.href = '/history/' + subscriberno;
        var title = "Subscription History data for "+subscriberno;
        //$("#messages").html(my_sess);
        $.colorbox({href:'/history/'+ subscriberno, title:title, width:"90%", height:"85%"});
    });
    $('#btnrenewhistory').click(function() {
        var subscriberno = $('#subscriberno').val();
        //window.location.href = '/renewhistory/' + subscriberno;
        var title = "Renewal History data for "+subscriberno;
        $.colorbox({href:'/renewhistory/'+ subscriberno, title:title, width:"90%", height:"85%"});
    });
    $('#id_service').change(function () {
	   service = $("#id_service").val();
	   if (service == '1') {
		  $("#id_bundles").prop("disabled", false);
		  $("#id_flashbundles").prop("disabled", true);
		  $("#id_devicebundles").prop("disabled", true);
		  $("#id_autorenew").prop("disabled", false);
	   } else {
		  $("#id_bundles").prop("disabled", false);
		  $("#id_flashbundles").prop("disabled", true);
		  $("#id_devicebundles").prop("disabled", true);  
		  $("#id_autorenew").prop("disabled", false);
	   }
	});
});

var showMessages = function(err, ok) { 
    $("#errmsg").remove();
    $("#progress").remove();    
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
    $("#loading").css({visibility:"visible"}).css({opacity:"1"})
    //.css({display:"block"})
}

var hideLoading = function() { $("#loading").fadeTo(1000, 0); };

var goBackToParent = function(url) { window.location.href = url; } 

function goBackToHome() { window.parent.location.href = '/'; }

function isNumber(n) {
    return !isNaN(parseFloat(n)) && isFinite(n);
}

$(document).ready(function() {
    //$('.popup_block').remove();
    loadPackages();
    $("#btnadd").colorbox({inline:true, width:"50%", href:"#popup1"});
});

$(document).ajaxSend(function (event, request, settings) {
    $('#addSubscription').hide();
	showLoading();
});

$(document).ajaxComplete(function (event, request, settings) {
    $('#addSubscription').show();
	hideLoading();
});
