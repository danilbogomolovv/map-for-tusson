import requests
#params =  {"cmemo":"oghk"}
terminal = { "cimei": "2", "inr": "2",
    "ctid": "fdgdf",
    "cmid": "2",
    "cpodr": "2",
    "cadres": "2",
    "cgorod": "2",
    "cobl": "2",
    "craion": "2",
    "ddatan": None,
    "cname": "2",
    "cparta": "2",
    "cots": "2",
    "czona": "2",
    "zona_name": "2",
    "cvsoba": "2",
    "cunn": "2",
    "cbank": "2",
    "ctype": "2",
    "right_adres": "2",
    "ss_nom": "2",
    "ddatap": None,
    "cmemo": "2",
    "cstatus": None,
    "lat": "2",
    "lng": "2"
}
params = {"ctid": "21"}
headers = {"Content-Type": "application/json"}

response = requests.post("http://localhost:8000/api/terminals/", headers = headers, params = terminal)
print(response.text)