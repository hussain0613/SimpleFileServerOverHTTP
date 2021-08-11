function get_contents(callBack){
    // fetch contents from server and then call callback
    xhr = new XMLHttpRequest()
    xhr.open("get", "/get_contents/?dir_path="+document.location.pathname, true)
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
    callBack(settings)
}

