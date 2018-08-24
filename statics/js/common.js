/**
 * Created by Administrator on 2018-8-1.
 */


document.write("<script type='text/javascript' src='/statics/js/jquery.min.js'></script>");

function test_onchange(self) {
    $("#id_url option").removeAttr("selected");
    var z = $("#id_url").val();
    console.log(z);
    for (var i=0;i<z.length;i++)
    {

    }
    // $("#id_url").val()
}


function test_lb_status(self) {
        console.log(1);
            // $.post("{% url 'test_lb_status' %}", {
            //                 "csrfmiddlewaretoken": "{{ csrf_token }}"
            //             }, function (callback) {
            //                 console.log(callback)
            //             });
        }
