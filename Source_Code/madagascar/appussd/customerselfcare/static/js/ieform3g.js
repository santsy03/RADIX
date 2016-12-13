function loadPackages() {
    $.ajax({
        type: 'GET',
        url: '/json/packages',
        dataType: 'json',
        success: function(json) {
            $('#id_bundles').empty();
            $('#id_flashbundles').empty();
            $('#id_devicebundles').empty();
            var elData = JSON.parse(json);
            $.each(elData, function(i, record) {
                cat_id = record.fields.category_id;
                if (cat_id == 1) {
                    $('#id_bundles')
                        .append($("<option></option>")
                        .attr("value", record.fields.id)
                        .text(record.fields.package_name + ' - MWK ' + (record.fields.package_cost )));
                }else if (cat_id == 2) {
                    $('#id_flashbundles')
                        .append($("<option></option>")
                        .attr("value", record.fields.id)
                        .text(record.fields.package_name + ' - MWK ' + (record.fields.package_cost )));
                }else if (cat_id == 3) {
                    $('#id_devicebundles')
                        .append($("<option></option>")
                        .attr("value", record.fields.id)
                        .text(record.fields.package_name + ' - MWK ' + (record.fields.package_cost )));
                }

            });
        },
        error: function(err) {
                //alert("Error Loading Package List");
                $("#messages").html("Error Loading Package List" + err.Message);
        }
    });
}

