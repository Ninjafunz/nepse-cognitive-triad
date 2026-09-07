"""T+2 Settlement calculation and business day progression for NEPSE."""

from datetime import date, timedelta
from typing import Set


class T2SettlementEngine:
    """Implements T+2 settlement logic respecting Nepal Stock Exchange trading schedules.
    NEPSE Trading Days: Sunday through Thursday.
    Closed Days: Friday and Saturday (Nepal weekend).
    """

    def __init__(self, public_holidays: Set[date] = None):
        self.public_holidays = public_holidays or set()

    def is_business_day(self, d: date) -> bool:
        """Friday (weekday 4) and Saturday (weekday 5) are market off days in Nepal."""
        if d.weekday() in (4, 5):
            return False
        if d in self.public_holidays:
            return False
        return True

    def calculate_settlement_date(self, trade_date: date) -> date:
        """Calculates T+2 settlement date.
        Must advance 2 active NEPSE business days from the trade date.
        """
        curr = trade_date
        settlement_days_added = 0

        while settlement_days_added < 2:
            curr += timedelta(days=1)
            if self.is_business_day(curr):
                settlement_days_added += 1

        return curr


t2_engine = T2SettlementEngine()
