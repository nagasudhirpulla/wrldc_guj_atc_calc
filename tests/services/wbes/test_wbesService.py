import datetime as dt
import unittest

from src.config.appConfig import loadAppConfig
from src.services.wbes.wbesService import fetchIsgsGenFullSch


class TestWbesService(unittest.TestCase):
    def test_run(self) -> None:
        appConf = loadAppConfig()
        genId = appConf["sellerId"]
        targetDt = dt.datetime.now()
        resp = fetchIsgsGenFullSch(targetDt, genId, None)
        self.assertTrue(isinstance(resp, list))
        self.assertFalse(len(resp) == 0)
