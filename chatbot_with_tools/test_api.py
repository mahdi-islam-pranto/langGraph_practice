import requests

url = "https://jobs-api14.p.rapidapi.com/v2/linkedin/search"

querystring = {"query":"Laravel","experienceLevels":"intern;entry;associate;midSenior;director","workplaceTypes":"remote;hybrid;onSite","location":"Bangladesh","datePosted":"month","employmentTypes":"contractor;fulltime;parttime;intern;temporary"}

headers = {
	"x-rapidapi-key": "1fe1f28520msh1e8fbf05c7c6a94p1a35ecjsnd51a81fb3246",
	"x-rapidapi-host": "jobs-api14.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())