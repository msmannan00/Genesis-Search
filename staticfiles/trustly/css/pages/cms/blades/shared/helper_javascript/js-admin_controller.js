class admin_controller {
    view_raw_json(){
        let m_result = document.getElementById(DOM.S_RESULT_CONTAINER).value;
        let myjson = JSON.stringify(JSON.parse(m_result), null, 2);
        console.log(myjson);

        let tab = window.open('about:blank', '_blank');
        tab.document.write('<html><body><pre>' + myjson + '</pre></body></html>'); // where 'html' is a variable containing your HTML
        tab.document.close();
    }
}

let m_admin_controller = new admin_controller();
function onTriggerScript(p_command){
    if (COMMANDS.S_RAW_JSON === p_command){
        m_admin_controller.view_raw_json()
    }
}

window.onload = function() {
    let m_java_error = document.getElementById(DOM.S_JAVA_ERROR)
    m_java_error.style.visibility = "hidden";
    m_java_error.style.marginBottom = "-35px";

    let m_result = document.getElementById(DOM.S_RESULT_CONTAINER).value;
    let m_json = JSON.parse(m_result);
    let m_response = self.json_tree(m_json)
    $('#m_result_success_display').html(m_response + "</ul>");
}
