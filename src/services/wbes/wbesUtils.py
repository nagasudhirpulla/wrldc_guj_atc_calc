import datetime as dt
import json
import re
from typing import List, Optional

import requests


# get default headers for requests
def getDefaultReqHeaders():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3887.7 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }


# get max rev for selected date
def getMaxRevForDate(baseUrl: str, revDt: dt.datetime):
    headers = getDefaultReqHeaders()
    # TODO set base url as app config
    revUrl = (
        "{0}/Report/GetCurrentDayFullScheduleMaxRev?regionid=2&ScheduleDate={1}".format(
            baseUrl, dt.datetime.strftime(revDt, "%d-%m-%Y")
        )
    )
    r = requests.get(revUrl, headers=headers)
    maxRevObj = r.json()
    return maxRevObj["MaxRevision"]


# convert the response dataArray to the schedule entry rows
# dataArray headers are in first 2 rows.
# first 2 columns of first header are 'Time Block' and 'Time Desc', next columns are all generator columns
# last column is grand total and need not be considered
# second header columns contain the schedule component description
# data starts from index 2 to index 97
# the dimension of the data array is to be 102x343
def convertDataArrayToSchRows(dataArray, targetDt):
    dataRows = []
    # check for the dimension of dataArray
    if len(dataArray) != 101:
        return []
    if len(dataArray[0]) < 3:
        return []
    for blk in range(1, 97):
        rowNum = blk
        for colIter in range(2, len(dataArray[0]) - 1):
            genName = dataArray[0][colIter]
            schVal = dataArray[rowNum][colIter]
            dataRows.append(
                {
                    "block": blk,
                    "val": float(schVal),
                    "sch_date": dt.datetime.strftime(targetDt, "%Y-%m-%d"),
                }
            )
    return dataRows


# download isgs generator full sch for a date from wbes reports
def getIsgsGenSchRowsForDate(
    baseUrl: str,
    targetDt: dt.datetime,
    sellerId: str = "ALL",
    revNum: Optional[int] = None,
) -> List[object]:
    rev = revNum
    # get max rev of day if rev number not specified
    if revNum == None:
        rev = getMaxRevForDate(baseUrl, targetDt)
    headers = getDefaultReqHeaders()
    # TODO keep base url as app config
    schUrl = "{0}/ReportFullSchedule/GetFullInjSummary?scheduleDate={1}&sellerId={2}&revisionNumber={3}&regionId=2&byDetails=0&isDrawer=0&isBuyer=0".format(
        baseUrl, dt.datetime.strftime(targetDt, "%d-%m-%Y"), sellerId, rev
    )
    r = requests.get(schUrl, headers=headers)
    resText = r.text
    # extract data array from the response
    jsonText = re.search("var data = JSON\.parse\((.*)\);", resText).group(1)
    # jsonText = jsonText.replace('\\', '')
    dataArray = json.loads(eval(jsonText))
    dataRows = convertDataArrayToSchRows(dataArray, targetDt)
    return dataRows
