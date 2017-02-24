from flask import render_template, flash, redirect
from flask import send_from_directory
from flask import request
from app import app
from bfValidation import BuildFinderForm
from rtLib import rtLib

import json
import requests
import grequests
from rtGetTasks import rtGetTasks


def exception_handler(request, exception):
    print 'Request failed: %s - %s - %s' % (request.url, request.response, exception)
    return True


@app.route('/')
@app.route('/jag')
def jag():
    allJobsList = []
    newJobsList = []
    hostList = []
    allStatuses = {'pass': 'blue', 'failed': 'red', 'running': '_anime', 'disabled': 'disabled'}

    if request.args.get('master') is not None:
        hostList.append(request.args.get('master'))
    else:
        hostList = app.config['JENKINS_URLS']

    for ip in hostList:
        try:
            print 'Attempting to talk to %s' % ip
            response = requests.get('http://%s/api/json' % ip, timeout=0.5)
        except Exception, e:
            print 'Failed to get jobs list from %s' % ip
            continue

        # Get all jobs
        if(response.status_code == 200):
            jsonResponse = json.loads(response.text)
            for jobs in jsonResponse['jobs']:
                jobs['origin'] = ip
                allJobsList.append(jobs)

        # Get all jobs with the specified status
        if request.args.get('status') is not None:
            status = request.args.get('status')
            for job in allJobsList:
                if allStatuses[status] in job['color']:
                    newJobsList.append(job)
            allJobsList = newJobsList

    if False:
        poolSize = 150
        # print [jobs['url'] + 'api/json' for jobs in allJobsList]
        jobList = []
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'}
        for u in allJobsList:
            jobList.append(u['url'] + 'api/json')
        rs = (grequests.get(job, timeout=3, stream=False, headers=headers) for job in jobList)

        responses = grequests.map(rs, exception_handler=exception_handler, size=poolSize)
        print responses

        for resp in responses:
            try:
                resp.close()
                jsonData = json.loads(resp.content)
                print 'Last build is ' + str(jsonData['lastBuild'])
            except Exception, e:
                # print e
                # print 'Cannot find last build'
                # print jsonData['name']
                continue

    # for job in allJobsList:
    #     try:
    #         URL = '%s/api/json' % job['url']
    #         response = requests.get(job['url'] + '/api/json', timeout=0.5)
    #         print response
    #     except:
    #         print 'Something went wrong'

    # print json.dumps(allJobsList, sort_keys=True, indent=4, separators=(',', ': '))
    print 'Total number of jobs: %s' % len(allJobsList)

    return render_template('jag.html',
                           title='Jenkins',
                           current_host=request.args.get('master'),
                           hosts=app.config['JENKINS_URLS'],
                           items=allJobsList,
                           statuses=allStatuses)


@app.route('/buildFinder', methods=['GET', 'POST'])
def buildFinder():
    rt = rtLib()
    form = BuildFinderForm()
    if request.method == 'POST':
        print form.validate_on_submit()
        print 'I got %s' % form.packageFileName.data
        flash('Your message! %s' % form.packageFileName.data)
        buildList = rt.getBuildRuns(form.packageFileName.data)
        # print buildList
        return render_template('buildFinder.html',
                               title='Build Finder',
                               buildList=sorted(buildList, reverse=True),
                               form=form)

    if request.method == 'GET':
        try:
            jsonData = requests.get('http://artifactory.devops.lab/artifactory/api/builds', timeout=10)
            buildData = json.loads(jsonData.text)
            buildList = set()
            for items in buildData['pagingData']:
                if items['buildName'] not in buildList:
                    buildList.add(items['buildName'])
        except Exception, e:
            print 'Failed to get builds list %s' % jsonData.status_code
            return 'Server error'

    return render_template('buildFinder.html',
                           title='Build Finder',
                           buildList=[],
                           form=form)


@app.route('/rtDash', methods=['GET'])
def rtDash():
    mesgList, mesgDict = rtGetTasks().main()
    return render_template('rtDash.html', title='Artifactory Dashboard', list=mesgList, dict=mesgDict)


@app.route('/mepview', methods=['GET'])
def mepViewer():
    return render_template('mepview.html', title='MEP Viewer')
