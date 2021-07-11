
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




function addParam(name, parta, status, check) {
    if (name != '') {
        localStorage.setItem('name', name);
    };
    if (parta != '' && availableparts.includes(parta)) {
        localStorage.setItem('parta', parta);
    };

    if (status != '') {
        localStorage.setItem('status', status);
    };
    let href_name = encodeURIComponent(localStorage.getItem('name'));
    let href_parta = encodeURIComponent(localStorage.getItem('parta'));
    let href_status = encodeURIComponent(localStorage.getItem('status'));

    if (check) {
        window.location.href = '/search/?name=' + href_name + '&parta=' + href_parta + '&status=' + href_status;
        } else { 
            if (availableparts.includes(parta)) {
              window.location.href = '/search/?name=' + href_name + '&parta=' + href_parta + '&status=' + href_status;  
            }

    }
}

function clearHref(){
    localStorage.setItem('parta', '');
    localStorage.setItem('name', '');
    localStorage.setItem('status', '');
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
