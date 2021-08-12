function create_row(path, content){
    //let content = contents[key]
    if(path[0] != "/" && path[0] != "\\") path = "/" + path 

    let img = document.createElement("img")
    img.classList.add("content_icon")
    if(content["is_directory"] == true){
        img.src = "/statics/res/folder.svg"
    }else {
        img.src = "/statics/res/download-file.svg"
    }
    
    let a = document.createElement("a")
    a.href = "/fs" + path
    let a_innerText = document.createElement("span")
    a_innerText.innerText = content["name"]

    let td1 = document.createElement("td")
    a.appendChild(img)
    a.appendChild(a_innerText)
    td1.appendChild(a)

    let td2 = document.createElement("td")
    td2.innerHTML = content["size"]? content["size"]:"-"
    td2.classList.add("text_center_align")

    let td3 = document.createElement("td")
    td3.innerHTML = content["date"]? content["date"]:"-"
    td3.classList.add("text_center_align")


    
    let td4 = document.createElement("td")
    td4.classList.add("text_right_align")
    if(content["is_directory"] != true){ // will add directories here too hopefully
        let download_icon = document.createElement("img")
        download_icon.classList.add("content_icon")
        download_icon.classList.add("non_button_button")
        download_icon.src = "/statics/res/download.svg"
        if(content["is_directory"] == true){
            download_icon.onclick = function(event){
                add_msg("Preparing " + path + "for download. It might take a while.")
            }
        }

        let aa = document.createElement("a")
        aa.href = "/download?path=" + path
        aa.appendChild(download_icon)

        td4.appendChild(aa)
    }

    if (content["directory"] != null){
        let dir_a = document.createElement("a")
        dir_a.innerText = "[visit dir]"
        dir_a.href = (content["directory"][0] == "/" || content["directory"][0] == "\\")? `/fs${content["directory"]}` : `/fs/${content["directory"]}`
        
        td4.appendChild(dir_a)
    }

    let row = document.createElement("tr")
    row.classList.add("content_row")
    
    row.appendChild(td1)
    row.appendChild(td2)
    row.appendChild(td3)
    row.appendChild(td4)

    let contents_tbody = document.querySelector("#contents_table>tbody")
    contents_tbody.appendChild(row)
}


function render_tbody(data){
    let contents_tbody = document.querySelector("#contents_table>tbody")

    contents_tbody.innerHTML = ""
    document.getElementById("current_directory_path_span").innerText = data["current_directory"]
    
    // actually rendering table
    if(data["parent_directory"] != null){
        create_row(data["parent_directory"], {"name": "Parent Directory", "is_directory": true})
    }

    for (let key in data["contents"]){
        create_row(key, data["contents"][key])
    }
}



function action_divs_display_toggle(div, div2, div3, div4){
    if(div.style.display == "none"){
        div.style.display = "block"
        div2.style.display = "none"
        div3.style.display = "none"
        div4.style.display = "none"
    }else{
        div.style.display = "none"
    }
}

function upload_files_div_display_toggle_wrapper(){
    let div = document.getElementById("upload_files_div")
    let div2 = document.getElementById("upload_folder_div")
    let div3 = document.getElementById("create_file_div")
    let div4 = document.getElementById("create_folder_div")
    action_divs_display_toggle(div, div2, div3, div4)
}

function upload_folder_div_display_toggle_wrapper(){
    let div = document.getElementById("upload_folder_div")
    let div2 = document.getElementById("create_file_div")
    let div3 = document.getElementById("create_folder_div")
    let div4 = document.getElementById("upload_files_div")
    action_divs_display_toggle(div, div2, div3, div4)
}

function create_files_div_display_toggle_wrapper(){
    let div = document.getElementById("create_file_div")
    let div2 = document.getElementById("upload_files_div")
    let div3 = document.getElementById("create_folder_div")
    let div4 = document.getElementById("upload_folder_div")
    action_divs_display_toggle(div, div2, div3, div4)
}
function create_folder_div_display_toggle_wraper(){
    let div = document.getElementById("create_folder_div")
    let div2 = document.getElementById("create_file_div")
    let div3 = document.getElementById("upload_files_div")
    let div4 = document.getElementById("upload_folder_div")
    action_divs_display_toggle(div, div2, div3, div4)
}


let message_count = 0

function add_msg(msg_string){
    document.getElementById("msg_div_display_toggle_btn").innerText = "Hide Messages"
    document.getElementById("msg_div").style.display = "block"

    message_count += 1

    let msg_li = document.createElement("li")
    msg_li.id = "msg_"+message_count
    msg_li.innerHTML = "[" +(new Date()).toLocaleString() + "] \t" + msg_string
    
    document.getElementById("msg_ul").appendChild(msg_li)
    return message_count
}

function update_msg(msg_serial, msg_string){
    document.getElementById("msg_div_display_toggle_btn").innerText = "Hide Messages"
    document.getElementById("msg_div").style.display = "block"
    
    let msg_li = document.getElementById("msg_"+msg_serial)
    msg_li.innerHTML = "[" +(new Date()).toLocaleString() + "] \t" + msg_string
}


function toggle_msg_div_display(){
    let msg_div_display_toggle_btn = document.getElementById("msg_div_display_toggle_btn")
    let msg_div = document.getElementById("msg_div")
    if(msg_div.style.display == "none"){
        msg_div.style.display = "block"
        msg_div_display_toggle_btn.innerText = "Hide Messages"
    }
    else {
        msg_div.style.display = "none"
        msg_div_display_toggle_btn.innerText = "Show Messages"
    }
}

function clear_messages(){
    document.getElementById("msg_ul").innerHTML = ""
}



function settings_dependent_tasks(settings){
    if(settings["upload_permission"] == true){
        let upload_files_toggle_btn = document.querySelector("#actions_menu>button")
        upload_files_toggle_btn.style.display = "inline"
        
    
        // let upload_folder_toggle_btn = document.querySelector("#actions_menu>button:nth-child(2)")
        // upload_folder_toggle_btn.style.display = "inline"
        
    
        // let create_file_toggle_btn = document.querySelector("#actions_menu>button:nth-child(3)")
        // create_file_toggle_btn.style.display = "inline"
        
    
        let create_folder_toggle_btn = document.querySelector("#actions_menu>button:nth-child(4)")
        create_folder_toggle_btn.style.display = "inline"
    }
}


function on_search(event){
    event.preventDefault()
    let query = document.getElementById("search_query_field").value
    let is_full = document.getElementById("search_checkbox").checked
    let dir_path = "/"
    console.log(is_full)
    if(is_full === false) dir_path = document.location.pathname.substring(3)

    get_search_result(query, dir_path)

}

