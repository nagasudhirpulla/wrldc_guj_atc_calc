from flask import Flask, render_template, request
from waitress import serve
from src.config.appConfig import loadAppConfig
from src.app.getImportCapForDate import getImportCapForDate
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound
import pandas as pd
import datetime as dt
from typing import Any, cast

# get application config
appConf = loadAppConfig()

# create server
app = Flask(__name__)
appPrefix = appConf["appPrefix"]
if pd.isna(appPrefix):
    appPrefix = ""
app.secret_key = appConf['flaskSecret']


@app.route('/', methods=['GET', 'POST'])
def index():
    schRows = None
    inpDtStr = dt.datetime.strftime(
        dt.datetime.now()+dt.timedelta(days=1), "%Y-%m-%d")
    if request.method == 'POST':
        inpDtStr = request.form['targetDt']
        targetDt = dt.datetime.strptime(inpDtStr, "%Y-%m-%d")
        schDf = getImportCapForDate(targetDt)
        schRows = schDf.to_dict("records")
    return render_template('home.html.j2', schRows=schRows, inpDtStr=inpDtStr)


hostedApp = Flask(__name__)
cast(Any, hostedApp).wsgi_app = DispatcherMiddleware(NotFound(), {
    appPrefix: app
})

if __name__ == '__main__':
    serverMode: str = appConf['mode']
    if serverMode.lower() == 'd':
        hostedApp.run(host="0.0.0.0", port=int(
            appConf['flaskPort']), debug=True)
    else:
        serve(app, host='0.0.0.0', port=int(
            appConf['flaskPort']), url_prefix=appPrefix, threads=1)
