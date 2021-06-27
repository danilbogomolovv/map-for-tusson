

function addParam(name, parta, zone, check) {
    if (name != '') {
        localStorage.setItem('name', name);
    };
    if (parta != '' && availableparts.includes(parta)) {
        localStorage.setItem('parta', parta);
    };
    if (zone != '') {
        localStorage.setItem('zone', zone);
    };

    let href_name = encodeURIComponent(localStorage.getItem('name'));
    let href_parta = encodeURIComponent(localStorage.getItem('parta'));
    let href_zone = encodeURIComponent(localStorage.getItem('zone'));
    if (check) {
        window.location.href = '/search/?name=' + href_name + '&parta=' + href_parta + '&zone=' + href_zone;
        } else { 
            if (availableparts.includes(parta)) {
              window.location.href = '/search/?name=' + href_name + '&parta=' + href_parta + '&zone=' + href_zone;  
            }

    }
}

function clearHref(){
    localStorage.setItem('parta', '');
    localStorage.setItem('name', '');
    localStorage.setItem('zone', '');
    window.location.href = '/';
}

function openfilterform() {
    document.getElementById('filterform').style.display = 'block'
}

$( function() {
$( "#parts" ).autocomplete({
  source: availableparts
});

  }
);
