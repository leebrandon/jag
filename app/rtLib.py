import requests
import json
import urllib

RT_TIMEOUT = 10


class rtLib():
    def setRtUrl(self, URL):
        self.rtUrl = URL
        return self.rtUrl

    def getBuildRuns(self, buildName):
        try:
            URL = '%s/api/build/%s' % (self.rtUrl, buildName)
            data = requests.get(URL, timeout=RT_TIMEOUT)
            tempData = json.loads(data.text)
            buildData = set()
            for item in tempData['buildsNumbers']:
                buildData.add(urllib.unquote(item['uri']).decode('utf8').split('::')[0][1:])

            print 'I found %s items ' % len(buildData)
            return buildData
        except Exception, e:
            print 'Failed: %s' % data.status_code

        return []
