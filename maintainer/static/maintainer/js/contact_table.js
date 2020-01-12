// Call the dataTables jQuery plugin
$(document).ready(function() {
    $('#dataTable').DataTable();
});


$(document).ready(function() {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    var table = $('#mdataTable').DataTable({
        dom: 'Bfrtip',
        select: true,
        buttons: {
            dom: {
                button: {
                    tag: 'button',
                    className: ''
                }
            },
            buttons: [
                { extend: 'selectAll', className: 'btn btn-info options' },
                { extend: 'selectNone', className: 'btn btn-info options' },
                {
                    text: 'Send mail',
                    action: function() {
                        var emails = [];
                        var count = table.rows({ selected: true }).count();
                        var data = table.rows({ selected: true }).data();
                        for (i = 0; i < count; i++) {
                            emails.push(data[i][1])
                        };
                        // Removing contact data of entries once mail is sent.
                        table.rows({ selected: true }).remove().draw();
                        $.ajax({
                            url: 'mcontact',
                            type: 'POST',
                            data: { 'emails': emails, 'req': 'sendmail' },
                            success: function(data) {
                                // console.log(data);
                            }

                        });
                    },
                    className: 'btn btn-success options'

                },

                {
                    text: 'Delete',
                    action: function() {
                        var deletion = [];
                        var count = table.rows({ selected: true }).count();
                        var data = table.rows({ selected: true }).data();
                        dele = {}
                        for (i = 0; i < count; i++) {
                            deletion.push(data[i][1])
                        };
                        var response = confirm("Are you sure you want to continue? Changes can't be undone");
                        if (response == true) {
                            table.rows({ selected: true }).remove().draw();
                            $.ajax({
                                url: 'mcontact',
                                type: 'POST',
                                data: { 'deletion': deletion, 'req': 'delete' },
                                success: function(data) {
                                    // console.log(data);
                                }

                            });
                        }
                    },
                    className: 'btn btn-danger options'

                },
                ,
                { extend: 'excel', className: 'btn btn-dark options', text:'Export as CSV' }

            ],
        },
        'columnDefs': [{
            'targets': 0,
            'orderable': false,
            'className': 'select-checkbox',
            'checkboxes': {
                'selectRow': true
            }
        }],
        'select': {
            'style': 'multi',
        }
    });


});