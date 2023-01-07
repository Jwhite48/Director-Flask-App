function submitButton(){
    if(document.getElementById('director_name').value.length > 1){
        document.getElementById('submit_button').style.display = "none";
        document.getElementById('loading_button').style.display = "block";
    }
}

function pickDirectorButton(movies, id){
    document.getElementById(`director_button${id}`).style.display = "none";
    document.getElementById(`loading_button${id}`).style.display = "flex";

    buttons = document.getElementsByClassName('director_buttons');
    for(let i=0; i<buttons.length; i++){
        if(buttons[i].id != `director_button${id}`){
            buttons[i].disabled = true;
        }
    }

    ret = '';
    for(let i=0; i<movies.length; i++){
        ret += movies[i]['id'];
        if(i != movies.length-1) ret += ",";
    }
    document.getElementById(`info_movies${id}`).value = ret;
}