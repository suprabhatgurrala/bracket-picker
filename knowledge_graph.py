"""Example of Python client calling Knowledge Graph Search API."""
import json
import urllib

api_key = 'AIzaSyBjzE-FnCh--LcKsrPYfjU0BQZMK20cNuo'
query = "Florida A&M"
service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
params = {
    'query': query + " basketball",
    'limit': 10,
    'indent': True,
    'prefix': True,
    'key': api_key,
    'types': "SportsTeam"
}
url = service_url + '?' + urllib.urlencode(params)
response = json.loads(urllib.urlopen(url).read())
if len(response['itemListElement']) > 0:
        for element in response['itemListElement']:
            print element['result']['name'] + ' (' + str(element['resultScore']) + ')'