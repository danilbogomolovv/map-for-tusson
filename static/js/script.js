
window.onload = function() {
checkboxes = document.getElementsByName('zones');

  for(var i=0, n=checkboxes.length;i<n;i++) {
      if (localStorage.getItem(checkboxes[i].id) == 'true') {
        document.getElementById(checkboxes[i].id).setAttribute('checked', 'checked')
      }
  }
  zonesChecked()
  document.getElementsByName('first_input')[0].value = localStorage.getItem('startpoint')
  document.getElementsByName('waypoints_input')[0].value = localStorage.getItem('tids')
  document.getElementsByName('last_input')[0].value = localStorage.getItem('ednpoint')
  document.getElementsByName('time_of_departure_input')[0].value = localStorage.getItem('time_of_departure')
  document.getElementById('repair_form').style.display = localStorage.getItem('repair_form')
  document.getElementById('repair_tids').style.display = localStorage.getItem('repair_tids')
  document.getElementById('terminals_for_repair').style.width = localStorage.getItem('terminals_for_repair_width')
  document.getElementById('repair_form_make_button').style.display = localStorage.getItem('repair_form_make_button')
  document.getElementById('repair_form_clear_button').style.display = localStorage.getItem('repair_form_clear_button')

  
    localStorage.setItem('parta', '');
    localStorage.setItem('name', '');
    localStorage.setItem('cpodr', '');



}


function search_place() {
    var geocoder;
    geocoder = new google.maps.Geocoder();
    var address = document.getElementById('search_place').value;
    
    geocoder.geocode( { 'address': address}, function(results, status) {
      
      if (status == 'OK') {
        map.setCenter(results[0].geometry.location);

      } else {
        alert('Geocode was not successful for the following reason: ' + status);
      }
    });
    map.setZoom(16);
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

    //if (check) {
        window.location.href = '/search/?name=' + href_name + '&parta=' + href_parta + '&cpodr=' + href_cpodr;
/*        } else { 
            if (availableparts.includes(parta)) {
              window.location.href = '/search/?name=' + href_name + '&parta=' + href_parta + '&cpodr=' + href_cpodr;  
            }

    }*/
}

function addRouteParam() {
    let start = document.getElementsByName('first_input')[0].value
    let tids =  document.getElementsByName('waypoints_input')[0].value
    let end =  document.getElementsByName('last_input')[0].value
    let time_of_departure =  document.getElementsByName('time_of_departure_input')[0].value
    var time =  document.getElementById('full_time_int').textContent
    time = parseInt(time.split(' ')[0],10)

    if (start != '') {
        localStorage.setItem('startpoint', start);
    };
    if (tids != '') {
        localStorage.setItem('tids', tids);
    };

    if (end != '') {
        localStorage.setItem('ednpoint', end);
    };

    if (time_of_departure != '') {
        localStorage.setItem('time_of_departure', time_of_departure);
    };

    window.location.href = '/route/?start=' + start + '&end=' + end + '&time=' + time + '&time_of_departure=' + time_of_departure + '&ctid=' + tids;
}

function addChartParam(chart_name, chart_type){

    if (chart_name != '') {
        localStorage.setItem('chart_name', chart_name);
    };
   if (chart_type != '') {
        localStorage.setItem('chart_type', chart_type);
    };
/*    document.getElementById(localStorage.getItem('chart_type')).setAttribute("checked", "checked")
    alert(document.getElementById(localStorage.getItem('chart_type')).checked)*/
    let href_chart_name = encodeURIComponent(localStorage.getItem('chart_name'));
    let href_chart_type = encodeURIComponent(localStorage.getItem('chart_type'));
    window.location.href = '/charts/?chart_name=' + href_chart_name + '&chart_type=' + href_chart_type
}

function add_new_marker(latlng){

  window.location.href = '/add_new_marker/?latlng=' + latlng  +'&terminals=' + document.getElementById('terminals_for_add').value 
}

function open_add_terminal_to_marker(lat, lng){
  document.getElementById('add_terminal_to_marker').style.display = 'block'
  document.getElementById('grey_bg').style.display = 'block'
  document.getElementById('lat_add_inp').value = lat
  document.getElementById('lng_add_inp').value = lng  
}

function add_terminal_to_marker(lat, lng){
  window.location.href = '/add_terminal_to_marker/?lat=' + lat + '&lng=' + lng + '&terminals=' + document.getElementById('terminals_for_transfer').value  
}

function check_delete_marker(lat, lng){
  document.getElementById('check_for_delete_marker').style.display = 'block'
  document.getElementById('grey_bg').style.display = 'block'
  document.getElementById('lat_del_inp').value = lat
  document.getElementById('lng_del_inp').value = lng
}

function close_check_delete_marker(){
  document.getElementById('check_for_delete_marker').style.display = 'none'
  document.getElementById('grey_bg').style.display = 'none'
}

function close_add_terminal_to_marker(){
  document.getElementById('add_terminal_to_marker').style.display = 'none'
  document.getElementById('grey_bg').style.display = 'none'
}

function delete_marker(lat, lng){
  window.location.href = '/delete_marker/?lat=' + lat + '&lng=' + lng
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

    $( "#cpodrs" ).autocomplete({
      source: availablecpodr 
    });

    }
);
