import requests
import json
import urllib

ARTIFACTORY_URL = 'http://artifactory.devops.lab/artifactory'
RT_TIMEOUT = 10


class rtLib():
    def getBuildRuns(self, buildName):
        try:
            URL = '%s/api/build/%s' % (ARTIFACTORY_URL, buildName)
            data = requests.get(URL, timeout=RT_TIMEOUT)
            tempData = json.loads(data.text)
            buildData = set()
            for item in tempData['buildsNumbers']:
                buildData.add(urllib.unquote(item['uri']).decode('utf8').split('::')[0][1:])

            print 'I found %s items ' % len(buildData)
            return buildData
        except:
            print 'Failed: %s' % data.status_code

        return []
