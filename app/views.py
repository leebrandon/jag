from flask import render_template
from flask import send_from_directory
from flask import request
from app import app

import json
import requests

items = ['one', 'two', 'three', 'four', 'five', 'six', 'seven']


#@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Brandon'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user,
                           items=items)


@app.route('/images')
def images():
    return render_template('images.html',
                           title='Images',
                           items=items)


@app.route('/profile/<id>')
def profile(id):
    return render_template('profile.html',
                           id=id,
                           item='two')


@app.route('/media/<regex("([\w\d_/-]+)?.(?:jpe?g|gif|png)"):filename>')
def media_file(filename):
    return send_from_directory(app.config['MEDIA_THUMBNAIL_FOLDER'], filename)


@app.route('/')
@app.route('/jag')
def jag():
    allJobsList = []
    hostList = []

    if request.args.get('master') is not None:
        hostList.append(request.args.get('master'))
    else:
        hostList = app.config['JENKINS_URLS']

    for ip in hostList:
        response = requests.get('http://%s/api/json' % ip)
        if(response.status_code == 200):
            jsonResponse = json.loads(response.text)
            for jobs in jsonResponse['jobs']:
                jobs['origin'] = ip
                allJobsList.append(jobs)

    print 'Total number of jobs: %s' % len(allJobsList)

    return render_template('jag.html',
                           title='Jenkins',
                           current_host=request.args.get('master'),
                           hosts=app.config['JENKINS_URLS'],
                           items=allJobsList)
