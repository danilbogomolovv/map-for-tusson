
window.onload = function() {
checkboxes = document.getElementsByName('zones');

  for(var i=0, n=checkboxes.length;i<n;i++) {
    for (j in localStorage) {
      if (j == checkboxes[i].id && localStorage[j] == 'true') {
        document.getElementById(j).setAttribute('checked', localStorage[j])
      }
    } 
  }
}




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


function toggle(source) {
  checkboxes = document.getElementsByName('zones');
  for(var i=0, n=checkboxes.length;i<n;i++) {
    checkboxes[i].checked = source.checked;
  }
}

function zonesChecked(){
  checkboxes = document.getElementsByName('zones');
  for(var i=0, n=checkboxes.length;i<n;i++) {
    if (checkboxes[i].checked == true) {
      localStorage.setItem(checkboxes[i].id, true)
    }
    else {
      localStorage.setItem(checkboxes[i].id, false)
    }
  }
}

function clearfilters(){
    document.getElementById('cadres').value = ''
    document.getElementById('cgorods').value = ''
    document.getElementById('cnames').value = ''
    document.getElementById('parts').value = ''
    document.getElementById('zones').value = '' 
    document.getElementById('cbanks').value = ''
    document.getElementById('ctypes').value = ''
    document.getElementById('inrs').value = ''
    document.getElementById('ctids').value = ''
    document.getElementById('cunns').value = '' 
    document.getElementById('cvsobas').value = ''
}

$( function() {
    $( "#parts" ).autocomplete({
      source: availableparts
    });


    $( "#zones" ).autocomplete({
      source: availablezones
    });


    $( "#cnames" ).autocomplete({
      source: availablenames
    });


    $( "#inrs" ).autocomplete({
      source: availableinrs
    });

    $( "#cgorods" ).autocomplete({
      source: availablegorod
    });

    $( "#ctids" ).autocomplete({
      source: availablectids
    });

    $( "#cadres" ).autocomplete({
      source: availableadres
    });
    $( "#cunns" ).autocomplete({
      source: availablecunns
    });
    $( "#cvsobas" ).autocomplete({
      source: availablecvsobas
    });
    $( "#ctypes" ).autocomplete({
      source: availabletypes
    });
    $( "#cbanks" ).autocomplete({
      source: availablebanks
    });

    }
);
