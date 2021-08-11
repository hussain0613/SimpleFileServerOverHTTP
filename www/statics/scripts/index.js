// gathering data
let rdir = data["root_directory"]
let cdir = data["current_directory"]
let pdir = data["parent_directory"]
let contents = data["contents"]
let settings = permissions


// actions related works
if(settings["upload"] == true){
    let upload_files_toggle_btn = document.querySelector("#actions_menu>button")
    upload_files_toggle_btn.style.display = "inline"
    upload_files_toggle_btn.addEventListener("click", upload_files_div_display_toggle_wrapper)

    document.getElementById("upload_files_btn").addEventListener("click", function(event){
        event.preventDefault()
        //also got to call server comm functions
        add_msg("clicked for upload files")
        update_msg(message_count, "updated upload files msg")
        //fetch data again after the changes
        render_tbody(contents)
    })



    let upload_folder_toggle_btn = document.querySelector("#actions_menu>button:nth-child(2)")
    upload_folder_toggle_btn.style.display = "inline"
    upload_folder_toggle_btn.addEventListener("click", upload_folder_div_display_toggle_wrapper)

    document.getElementById("upload_folder_btn").addEventListener("click", function(event){
        event.preventDefault()
        //also got to call server comm functions
        add_msg("clicked for upload folder")
        update_msg(message_count, "updated upload folder msg")
        //fetch data again after the changes
        render_tbody(contents)
    })

    let create_file_toggle_btn = document.querySelector("#actions_menu>button:nth-child(3)")
    create_file_toggle_btn.style.display = "inline"
    create_file_toggle_btn.addEventListener("click", create_files_div_display_toggle_wrapper)

    let create_folder_toggle_btn = document.querySelector("#actions_menu>button:nth-child(4)")
    create_folder_toggle_btn.style.display = "inline"
    create_folder_toggle_btn.addEventListener("click", create_folder_div_display_toggle_wraper)



    document.getElementById("create_file_btn").addEventListener("click", function(event){
        event.preventDefault()
        //also got to call server comm functions
        add_msg("clicked for creating file")
        update_msg(message_count, "updated file creation msg")
        //fetch data again after the changes
        render_tbody(contents)
    })


    document.getElementById("create_folder_btn").addEventListener("click", function(event){
        event.preventDefault()
        //also got to call server comm functions
        add_msg("clicked for creating folder")
        update_msg(message_count, "updated folder creation msg")
        //fetch data again after the changes
        render_tbody(contents)
    })
}


render_tbody(contents)
document.getElementById("msg_div_display_toggle_btn").addEventListener("click", toggle_msg_div_display)
document.getElementById("clear_msgs_buttion").addEventListener("click", clear_messages)
