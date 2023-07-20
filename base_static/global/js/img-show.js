function preview () {
    frame.src = URL.createObjectURL(event.target.files[0]);
    document.querySelector('#frame').classList.add('frame-img')
}

function clearImage () {
    document.getElementById('formFile').value = null;
    frame.src = "";
    document.querySelector('#frame').classList.remove('frame-img');
}
