var widget;
window.onload = function() {
    widget = SC.Widget(document.getElementById('sc-widget'));
};

function playMusic(url) {
    widget.load(url, {auto_play: true});
}

function togglePlay() {
    widget.toggle();
}

function setVolume(value) {
    widget.setVolume(value);
}

function openEditModal(id, title, artist) {
    // Define a ação do form com a URL correta (ajuste conforme seu urls.py)
    const form = document.getElementById('editMusicForm');
    form.action = `/edit_music/${id}/`; // Verifique se este é o seu caminho
    
    // Preenche os campos
    document.getElementById('editTitle').value = title;
    document.getElementById('editArtist').value = artist;
    
    // Abre o modal do Bootstrap
    var myModal = new bootstrap.Modal(document.getElementById('editMusicModal'));
    myModal.show();
}

function openEditAlbumModal(id, name, musicIds) {
    document.getElementById('editAlbumId').value = id;
    document.getElementById('editAlbumName').value = name;
    
    // Desmarca todos antes de marcar os corretos
    document.querySelectorAll('.music-checkbox').forEach(cb => cb.checked = false);
    
    // Marca as músicas que já pertencem ao álbum
    musicIds.forEach(mId => {
        const checkbox = document.getElementById('editMusic' + mId);
        if (checkbox) checkbox.checked = true;
    });
    
    var myModal = new bootstrap.Modal(document.getElementById('editAlbumModal'));
    myModal.show();
}