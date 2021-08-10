function create_row(path, content){
    //let content = contents[key]
    
    let img = document.createElement("img")
    img.classList.add("content_icon")
    if(content["is_directory"] == true){
        img.src = "././res/folder.svg"
    }else {
        img.src = "././res/download-file.svg"
    }
    
    let a = document.createElement("a")
    a.href = path
    let a_innerText = document.createElement("span")
    a_innerText.innerText = content["name"]

    let td1 = document.createElement("td")
    //td1.appendChild(img)
    a.appendChild(img)
    a.appendChild(a_innerText)
    td1.appendChild(a)

    let td2 = document.createElement("td")
    td2.innerHTML = content["size"]? content["size"]:"-"
    td2.classList.add("text_center_align")

    let td3 = document.createElement("td")
    td3.innerHTML = content["date"]? content["date"]:"-"
    td3.classList.add("text_right_align")

    let row = document.createElement("tr")
    row.classList.add("content_row")
    
    row.appendChild(td1)
    row.appendChild(td2)
    row.appendChild(td3)

    let contents_tbody = document.querySelector("#contents_table>tbody")
    contents_tbody.appendChild(row)
}


function render_tbody(){
    let contents_tbody = document.querySelector("#contents_table>tbody")

    contents_tbody.innerHTML = ""
    // hudai
    if(rdir == cdir){
        document.getElementById("current_directory_path_span").innerText = "root"
    }else{
        document.getElementById("current_directory_path_span").innerText = data["current_directory"]
    }

    // actually rendering table
    if(pdir != null){
        create_row(pdir, {"name": "Parent Directory", "is_directory": true})
    }

    for (let key in contents){
        create_row(key, contents[key])
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
    message_count += 1

    let msg_li = document.createElement("li")
    msg_li.id = "msg_"+message_count
    msg_li.innerText = msg_string
    
    document.getElementById("msg_ul").appendChild(msg_li)
}

function update_msg(msg_serial, msg_string){
    let msg_li = document.getElementById("msg_"+msg_serial)
    msg_li.innerText = msg_string
}


function toggle_msg_div_display(){
    let msg_div_display_toggle_btn = document.getElementById("msg_div_display_toggle_btn")
    let msg_div = document.getElementById("msg_div")
    if(msg_div.style.display == "none"){
        msg_div.style.display = "block"
        document.getElementById("msg_div_display_toggle_btn").innerText = "Hide Messages"
    }
    else {
        msg_div.style.display = "none"
        document.getElementById("msg_div_display_toggle_btn").innerText = "Show Messages"
    }
}

function clear_messages(){
    document.getElementById("msg_ul").innerHTML = ""
}


