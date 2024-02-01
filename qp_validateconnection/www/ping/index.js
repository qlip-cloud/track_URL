$(document).ready(function() {

    if ( $("#ping-page").length ) {

        if ($("#ping-page").data("list_valid") > 0){

            delay = $("#ping-page").data("delay")

            active_ping()

            delay = delay * 1000;
        
            setInterval(exec_ping,delay)
        }
      }
    
});

function active_ping(){

    url = "qp_validateconnection.services.validate_status.validate_daemon"

    callback = ()=>{

    }
    send_petition(url, callback)


}
function exec_ping(){

    url = "qp_validateconnection.www.ping.index.search_ping"

    callback = (response)=>{
        response.forEach(element => {
            $(`#point-${element.name}`).removeClass().addClass(element.ping);
            $(`#text-${element.name}`).html(element.ping)
            $(`#text-${element.name}`).html(element.ping)
            $(`#date-${element.name}`).html(element.ping_refresh)
            
        });
    }

    send_petition(url, callback)
}


async function send_petition(url, callback = null){

    return new Promise(() => {
        frappe.call({
            method: url ,
            args: null,
            async: true,
            callback: function (r_1) {

                response = r_1.message
                
                callback(response)

            }
        })
    })
}