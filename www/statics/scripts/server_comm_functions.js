function get_contents(callBack){
    // fetch contents from server and then call callback
    xhr = new XMLHttpRequest()
    xhr.open("get", "/get_contents/?dir_path="+document.location.pathname.substring(3), true)
    xhr.onreadystatechange = function(){
        if(this.readyState == 4){
            if(this.status == 200){
                resp = JSON.parse(this.responseText)
                if(resp["status"] == "success"){
                    //console.log(resp["data"])
                    callBack(resp["data"])
                }else{
                    console.log(resp["details"])
                    add_msg(resp["details"])
                }
            }else{
                console.log("khaiso mara")
                add_msg("error fetching contetns. http status: "+ this.status)
            }
        }
    }

    xhr.send()
}


function get_settings(callBack){
    // fetch settings from server and then call callBack
    xhr = new XMLHttpRequest()
    xhr.open("get", "/get_settings/", true)
    xhr.onreadystatechange = function(){
        if(this.readyState == 4){
            if(this.status == 200){
                resp = JSON.parse(this.responseText)
                if(resp["status"] == "success"){
                    //console.log(resp["data"])
                    callBack(resp["settings"])
                }else{
                    console.log(resp["details"])
                    add_msg(resp["details"])
                }
            }else{
                console.log("khaiso mara")
                add_msg("error fetching settings. http status: "+ this.status)
            }
        }
    }

    xhr.send()
}


function upload_files(formdata){
    let xhr = new XMLHttpRequest()
    xhr.open("post", "/upload_files/?dir_path="+document.location.pathname.substring(3), true)
    
    let total_size = 0.0
    let msg_cnt = add_msg("preparing upload")
    
    xhr.upload.onloadstart = function(ev){
        update_msg(msg_cnt, "starting upload")
        total_size = Math.round(ev.total / (10**6)) // in MB
        total_size = total_size.toFixed(2) // rounding up to 2 decimal points
    }
    xhr.upload.onprogress = function(ev){
        var uploaded = ev.loaded/(10**6) // in MB
        var percentage = ev.loaded/ev.total * 100
        update_msg(msg_cnt, `uploaded: \t ${uploaded.toFixed(2)} of ${total_size}MB \t -- \t ${percentage.toFixed(2)}%`)
    }
    xhr.upload.onloadend = function(ev){
        var uploaded = ev.loaded/(10**6) // in MB
        var percentage = ev.loaded/ev.total * 100
        
        update_msg(msg_cnt, `upload complete \t ${uploaded.toFixed(2)} of ${total_size}MB \t -- \t ${percentage.toFixed(2)}%`)
    }

    msg_cnt2 = add_msg("Server reply: ")
    xhr.onreadystatechange = function(){
        if(this.readyState == 4){
            if(this.status == 200){
                resp = JSON.parse(this.responseText)
                if(resp["status"] == "success"){
                    // polution by directly calling ui functions in here
                    update_msg(msg_cnt2, "Server reply: "+ resp["details"])
                    get_contents(render_tbody)
                }else{
                    console.log(resp["details"])
                    update_msg(msg_cnt2, "Server reply: "+ resp["details"])
                }
            }else{
                console.log("khaiso mara")
                update_msg(msg_cnt2, "error uploading files. http resp status: "+ this.status)
            }
        }
    }

    xhr.send(formdata)
}



function create_folder(new_folder_name, callBack){
    // fetch settings from server and then call callBack
    xhr = new XMLHttpRequest()
    xhr.open("post", `/create_directory/?dir_path=${document.location.pathname.substring(3)}&new_dir_name=${new_folder_name}`, true)
    xhr.onreadystatechange = function(){
        if(this.readyState == 4){
            if(this.status == 200){
                resp = JSON.parse(this.responseText)
                if(resp["status"] == "success"){
                    //console.log(resp["data"])
                    get_contents(callBack)
                    add_msg(resp["details"])
                }else{
                    console.log(resp["details"])
                    add_msg(resp["details"])
                }
            }else{
                console.log("khaiso mara")
                add_msg("error creating folder. http status: "+ this.status)
            }
        }
    }
    xhr.send()
}


function get_search_result(query, dir_path){
    add_msg(`searching for ${query} in ${dir_path}... might take a while`)
    let msg_cnt = add_msg("server reply: ")
    xhr = new XMLHttpRequest()
    xhr.open("get", `/get_search_result/?query=${query}&dir_path=${dir_path}`, true)
    xhr.onreadystatechange = function(){
        if(this.readyState == 4){
            if(this.status == 200){
                resp = JSON.parse(this.responseText)
                if(resp["status"] == "success"){
                    //console.log(resp["data"])
                    render_tbody(resp["data"])
                    update_msg(msg_cnt, "server reply: " + resp["details"])
                    settings_dependent_tasks({"upload_permission": false})
                }else{
                    console.log(resp["details"])
                    update_msg(msg_cnt, "server reply: " + resp["details"])
                }
            }else{
                console.log("khaiso mara")
                update_msg(msg_cnt, "error creating folder. http status: " + this.status)
            }
        }
    }
    xhr.send()
}
