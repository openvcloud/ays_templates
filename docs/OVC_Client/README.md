### How to configure ovc client using AYS:

For using ovc client, you will need to configure itsyou.online client for one time at least then you can configure the OVC client

1 - Configure the main (and the only) instance of itsyouonline client 
```bash
curl --request POST \
  --url 'http://localhost:5000/ays/repository/{REPO_NAME}/configure-jslocation' \
  --header 'content-type: application/json' \
  --data '{
	"instance": "main",
	"jslocation": "j.clients.itsyouonline",
	"data": {
		"baseurl": "https://itsyou.online/api",
		"application_id_": "{CLIENT_ID}",
		"secret_": "{CLIENT_SECRET}"
	}
  }'
```
* You will need to replace `{REPO_NAME}` with your repo name and `{CLIENT_ID}`, `{CLIENT_SECRET}` with your itsyou.online API credentials
* You will need to pass authorization header if you are using ays in production mode

2 - Configure the ovc client
```bash
curl --request POST \
  --url 'http://localhost:5000/ays/repository/{REPO_NAME}/configure-jslocation' \
  --header 'content-type: application/json' \
  --data '{
	"instance": "main",
	"jslocation": "j.clients.openvcloud",
	"data": {
		"address": "{ENV_URL}"
	}
  }'
```
* You will need to replace `{REPO_NAME}` with your repo name and `{ENV_URL}` with env url (i.e. be-g8-3.demo.greenitglobe.com)
