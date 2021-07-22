import requests
#params =  {"cmemo":"oghk"}
terminal = { "cimei": "7", "inr": "7",
    "ctid": "fdgdf",
    "cmid": "7",
    "cpodr": "7",
    "cadres": "7",
    "cgorod": "7",
    "cobl": "7",
    "craion": "7",
    "ddatan": null,
    "cname": "7",
    "cparta": "7",
    "cots": "7",
    "czona": "7",
    "zona_name": "7",
    "cvsoba": "7",
    "cunn": "7",
    "cbank": "7",
    "ctype": "7",
    "right_adres": "7",
    "ss_nom": "7",
    "ddatap": null,
    "cmemo": "7",
    "cstatus": 0,
    "lat": "7",
    "lng": "7"
}
params = {"ctid": "71"}
headers = {"Content-Type": "application/json"}

response = requests.post("http://localhost:8000/api/terminals/", headers = headers, params = terminal)
print(response.text)