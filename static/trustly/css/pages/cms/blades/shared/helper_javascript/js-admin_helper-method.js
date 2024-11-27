function json_tree(object){
    let json = "<ul class='manage-json'>";
    for(const prop in object){
        const value = object[prop];
        switch (typeof(value)){
            case "object":
                const token = Math.random().toString(36).substr(2, 16);
                json += "<div class='manage-json'><a class='label badge badge-secondary manage-json-container' href='#"+token+"' data-toggle='collapse'><span class='manage-json-container--info-arow'>&#8609;&nbsp;&nbsp;</span> "+prop+"="+"m_object"+"</a><div id='"+token+"' class='collapse'>"+json_tree(value)+"</div></div>";break;default:
                json += "<div class='manage-json'><p class='label badge badge-info manage-json-container--info'>"+prop+"="+value+"</p></div>";
        }
    }
    return json+"</ul>";
}
