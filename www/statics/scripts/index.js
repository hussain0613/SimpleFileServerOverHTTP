get_settings(settings_dependent_tasks)
get_contents(render_tbody)


document.getElementById("msg_div_display_toggle_btn").addEventListener("click", toggle_msg_div_display)
document.getElementById("clear_msgs_buttion").addEventListener("click", clear_messages)


document.querySelector("#actions_menu>button").addEventListener("click", upload_files_div_display_toggle_wrapper)
document.getElementById("upload_files_form").addEventListener("submit", function(event){
    event.preventDefault()
    let formdata = new FormData(document.getElementById("upload_files_form"))
    upload_files(formdata)
})


// document.querySelector("#actions_menu>button:nth-child(2)").addEventListener("click", upload_folder_div_display_toggle_wrapper)
    
// document.getElementById("upload_folder_btn").addEventListener("click", function(event){
//     event.preventDefault()
//     //also got to call server comm functions
//     add_msg("clicked for upload folder")
//     update_msg(message_count, "updated upload folder msg")
//     //fetch data again after the changes
//     get_contents(render_tbody)
// })


// document.getElementById("create_file_btn").addEventListener("click", function(event){
//     event.preventDefault()
//     //also got to call server comm functions
//     add_msg("clicked for creating file")
//     update_msg(message_count, "updated file creation msg")
//     //fetch data again after the changes
//     get_contents(render_tbody)
// })


document.getElementById("create_folder_form").addEventListener("submit", function(event){
    event.preventDefault()
    create_folder(document.getElementById("folder_name").value, render_tbody)
    
})

document.querySelector("#actions_menu>button:nth-child(3)").addEventListener("click", create_files_div_display_toggle_wrapper)
document.querySelector("#actions_menu>button:nth-child(4)").addEventListener("click", create_folder_div_display_toggle_wraper)


document.getElementById("search_form").addEventListener("submit", on_search)
