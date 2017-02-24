import os
import sys
import requests
import json
import time


class rtGetTasks:
    rtUrl = 'http://artifactory.devops.lab/artifactory'
    creds = ('devops', 'mapr')
    validStates = ['running', 'scheduled', 'stopped']

    def getState(self, item):
        return item['state']

    def main(self):
        mesgList = []
        mesgDict = []
        URL = '%s/api/tasks' % self.rtUrl
        data = requests.get(URL, auth=self.creds, timeout=5)
        if data.status_code == 200:
            jsonData = json.loads(data.content)
            for item in jsonData['tasks']:
                # if item['state'] == 'running':
                taskType = item['type'].split('.')[-1]
                mesgList.append('Running: ' + item['description'])
                mesgDict.append({'state': item['state'], 'name': item['description'], 'id': item['id'], 'type': taskType})
        # print sorted(mesgDict, key=self.getState)
        return mesgList, sorted(mesgDict, key=self.getState)
