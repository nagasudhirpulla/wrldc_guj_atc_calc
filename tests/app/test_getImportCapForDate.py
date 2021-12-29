import datetime as dt
import unittest

import pandas as pd
from src.app.getImportCapForDate import getImportCapForDate
from src.config.appConfig import loadAppConfig


class TestAppLogic(unittest.TestCase):
    def test_run(self) -> None:
        appConf = loadAppConfig()
        targetDt = dt.datetime.now()
        resp = getImportCapForDate(targetDt)
        self.assertTrue(isinstance(resp, pd.DataFrame))
