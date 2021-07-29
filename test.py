import requests
#params =  {"cmemo":"oghk"}
terminal = { "cimei": "8", "inr": "8",
    "ctid": "fdgdf",
    "cmid": "8",
    "cpodr": "8",
    "cadres": "8",
    "cgorod": "8",
    "cobl": "8",
    "craion": "8",
    "ddatan": null,
    "cname": "8",
    "cparta": "8",
    "cots": "8",
    "czona": "8",
    "zona_name": "8",
    "cvsoba": "8",
    "cunn": "8",
    "cbank": "8",
    "ctype": "8",
    "right_adres": "8",
    "ss_nom": "8",
    "ddatap": null,
    "cmemo": "8",
    "cstatus": 0,
    "lat": "8",
    "lng": "8"
}
params = {"ctid": "81"}
headers = {"Content-Type": "application/json"}

response = requests.post("http://localhost:8000/api/terminals/", headers = headers, params = terminal)
print(response.text)