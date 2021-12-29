import datetime as dt
from typing import List, Optional

from src.services.wbes.wbesUtils import getIsgsGenSchRowsForDate
from src.config.appConfig import loadAppConfig


def fetchIsgsGenFullSch(
    targetDt: dt.datetime, genId: str, rev: Optional[int] = None
) -> List[object]:
    # TODO model the return type instead of List[object]
    appConf = loadAppConfig()
    return getIsgsGenSchRowsForDate(appConf["wbesBaseUrl"], targetDt, genId, rev)
