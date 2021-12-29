import datetime as dt

import numpy as np
import pandas as pd
from src.config.appConfig import getAppConfig
from src.services.wbes.wbesService import fetchIsgsGenFullSch


def getImportCapForDate(targetDt: dt.datetime):
    # get ssp sch for the date
    appConf = getAppConfig()

    # get seller id ssp
    sellerId = appConf["sellerId"]

    # fetch the isgs full schedule of ssp
    schRows = fetchIsgsGenFullSch(targetDt, sellerId)

    # convert results to dataframe
    schDf = pd.DataFrame(data=schRows)

    # sort by date and block number
    schDf = schDf.sort_values(by=["sch_date", "block"])

    # rename value column by the desired name
    schDf.rename(columns={"val": "SSP_Sch"}, inplace=True)

    # create reliability margin column
    schDf["RM"] = 330

    # create import TTC column
    schDf["Imp_TTC"] = np.nan
    schPresentFilter = (schDf["SSP_Sch"] > 0)
    # solar hrs is between 9 to 17 hrs
    solarHrsFilter = (schDf["block"] > 36) & (schDf["block"] <= 68)

    # populate values in the import TTC column
    schDf.loc[(schPresentFilter & solarHrsFilter), ["Imp_TTC"]] = 9830
    schDf.loc[(schPresentFilter & ~solarHrsFilter), ["Imp_TTC"]] = 10230
    schDf.loc[(~schPresentFilter & solarHrsFilter), ["Imp_TTC"]] = 9630
    schDf.loc[(~schPresentFilter & ~solarHrsFilter), ["Imp_TTC"]] = 10030

    # create import ATC column
    schDf["Imp_ATC"] = schDf["Imp_TTC"] - schDf["RM"]
    return schDf
