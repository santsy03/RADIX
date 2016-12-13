    $(function() {
        $("#from").datepicker({
            inline: true, dateFormat: "dd-mm-yy"
        });

        $("#to").datepicker({
            inline: true, dateFormat: "dd-mm-yy"
        });
    });

$(document).ready(function() {
    $("#auditsearch").submit(function(e) {
        var from = $('#from').val();
        var to = $('#to').val();
        var stext = $('#txtsearch').val();
        $("#results").empty();
        var csrftoken = $.cookie('csrftoken');
        var values = {'from': from, 'to': to, 'text': stext, 'csrfmiddlewaretoken': csrftoken };
        if (from == '' && to == '') {
            $("#results").html('Please provide start and end dates.');
            return false;
        }
        e.preventDefault();
        $("#results").html("<img src='/includes/images/ajax-loader.gif'/>");
        $.ajax({
            type: "POST",
            crossDomain: false,
            data: values,
            dataType: "json",
            url: "/audittrail/",
            success: function(data){
                //$('#results').html(data.message);
                if (data.length == 0) {
                    $('#results').html("No data for for this query");
                }else{
                    //$('#errmsg').html(data);
                    content = "<table width='100%' class='datagrid'>"
                    content += "<th>MSISDN</td>";
                    content += "<th>Amount</td>";
                    content += "<th>Service</td>";
                    content += "<th>Details</td>";
                    content += "<th>Date / Time</td>";
                    content += "<th>CC Agent</td>";
                    $.each(data, function(key, val) {
                        content += "<tr>"
                        content += "<td>" + data[key].msisdn + "</td>";
                        content += "<td>" + data[key].price + "</td>";
                        content += "<td>" + data[key].servicename + "</td>";
                        content += "<td>" + data[key].packagename + "</td>";
                        content += "<td>" + data[key].createddatetime + "</td>";
                        content += "<td>" + data[key].username + "</td>";
                        content += "</tr>";
                    });
                    if (stext != ''){
                        var qtext = "from "+from+" to "+to+" containing "+ stext;
                    }else{
                        var qtext = "from "+from+" to "+to;
                    }
                    var query = "?from="+from+"&to="+to+"&text="+stext;
                    var title = "History data for your query "+qtext+" | <a href='/export_audit/"+query+"'>Export ("+data.length+" records)</a>"
                    $.colorbox({html:content+"</table>", title:title, width:"90%", height:"85%"});
                    $("#results").empty();
                }
            },
            error: function(e){
                $("#results").html('Please refresh page and try again'+e);
        }
        });
    });
});
