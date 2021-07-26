
window.onload = function() {
checkboxes = document.getElementsByName('zones');

  for(var i=0, n=checkboxes.length;i<n;i++) {
    for (j in localStorage) {
      console.log(localStorage[j])
      if (j == checkboxes[i].id && localStorage[j] == 'true') {
        document.getElementById(j).setAttribute('checked', localStorage[j])
      }
    } 
  }

  document.getElementById('repair_form').style.display = localStorage.getItem('repair_form')
  document.getElementById('repair_tids').style.display = localStorage.getItem('repair_tids')
  document.getElementById('terminals_for_repair').style.width = localStorage.getItem('terminals_for_repair_width')
  document.getElementById('repair_form_make_button').style.display = localStorage.getItem('repair_form_make_button')
  document.getElementById('repair_form_clear_button').style.display = localStorage.getItem('repair_form_clear_button')
}


function ShowTerminalForRepairInfo(lat, lng, ddatap, cmemo, cparta, cadres) {
  var myLatlng = new google.maps.LatLng(lat, lng);
  map.setZoom(12);
  map.panTo(myLatlng);
  document.getElementById('terminals_for_repair_info').style.display = 'block'
  document.getElementById('terminals_for_repair_info').innerHTML = "<h5>Дата :</h5>" + ddatap  + "<h5>Информация :</h5>" + cmemo + "<h5>Партнер :</h5>" + cparta + "<h5>Адрес :</h5>" + cadres + '</br>    <button class="btn btn-outline-danger" onclick="ClearRepairInfo()">Сбросить</button> '
}

function ClearFormField(id) {
  document.getElementById(id).value = ''
}

function ShowFormCloseTids(){
  document.getElementById('repair_form').style.display = 'block'
  document.getElementById('repair_tids').style.display = 'none'
  document.getElementById('terminals_for_repair').style.width = '24%'
  document.getElementById('repair_form_make_button').style.display = 'block'
  document.getElementById('repair_form_clear_button').style.display = 'block'
  localStorage.setItem('repair_tids', 'none') 
  localStorage.setItem('repair_form', 'block')
  localStorage.setItem('terminals_for_repair_width', '24%') 
  localStorage.setItem('repair_form_make_button', 'block')
  localStorage.setItem('repair_form_clear_button', 'block')

}

function ShowTidsCloseForm(){
  document.getElementById('repair_tids').style.display = 'block'
  document.getElementById('repair_form').style.display = 'none'
  document.getElementById('terminals_for_repair').style.width = '16%'
  document.getElementById('repair_form_make_button').style.display = 'none'
  document.getElementById('repair_form_clear_button').style.display = 'none'
  localStorage.setItem('repair_tids', 'block') 
  localStorage.setItem('repair_form', 'none')
  localStorage.setItem('terminals_for_repair_width', '16%') 
  localStorage.setItem('repair_form_make_button', 'none')
  localStorage.setItem('repair_form_clear_button', 'none')
}

function ClearRepairInfo() {
  var myLatlng = new google.maps.LatLng(53.904789501846196, 27.553534868069242);
  map.setZoom(6);
  map.panTo(myLatlng); 
  document.getElementById('terminals_for_repair_info').style.display = 'none' 
}

function addParam(name, parta, cpodr, check) {
    if (name != '') {
        localStorage.setItem('name', name);
    };
    if (parta != '' && availableparts.includes(parta)) {
        localStorage.setItem('parta', parta);
    };

    if (cpodr != '') {
        localStorage.setItem('cpodr', cpodr);
    };
    let href_name = encodeURIComponent(localStorage.getItem('name'));
    let href_parta = encodeURIComponent(localStorage.getItem('parta'));
    let href_cpodr = encodeURIComponent(localStorage.getItem('cpodr'));

    if (check) {
        window.location.href = '/search/?name=' + href_name + '&parta=' + href_parta + '&cpodr=' + href_cpodr;
        } else { 
            if (availableparts.includes(parta)) {
              window.location.href = '/search/?name=' + href_name + '&parta=' + href_parta + '&cpodr=' + href_cpodr;  
            }

    }
}

function clearHref(){
    localStorage.setItem('parta', '');
    localStorage.setItem('name', '');
    localStorage.setItem('cpodr', '');
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

    // $( "#cadres" ).autocomplete({
    //   source: availableadres
    // });

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

    $( "#cpodrs" ).autocomplete({
      source: availablecpodr 
    });

    }
);
