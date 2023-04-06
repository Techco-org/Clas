function countCharacter(){
    let text = document.about_form.about.value;
    console.log(text);
    document.getElementById('characters').innerText = text.length;
}