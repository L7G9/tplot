from datetime import datetime

from date_time_timelines.models import (
    WEEK_1,
    MONTH_PREFIX,
    MONTH_1,
    MONTH_6,
    YEAR_PREFIX,
    YEAR_1,
    YEAR_1000
)
from timelines.pdf.time_unit import TimeUnit
from timelines.pdf.round import Round


def round_by_seconds(
    date_time: datetime,
    seconds_in_scale_unit,
    round: Round
) -> datetime:
    seconds = int(date_time.timestamp())
    multiples = seconds // seconds_in_scale_unit
    remainder = seconds % seconds_in_scale_unit
    if (remainder > 0) and round.up():
        multiples += 1

    return datetime.fromtimestamp(multiples * seconds_in_scale_unit)


def round_by_weeks(
    date_time: datetime,
    round: Round
) -> datetime:
    seconds_per_day = 24*60*60

    if (
        date_time.weekday() == 0
        and date_time.hour == 0
        and date_time.minute == 0
        and date_time.second == 0
    ):
        return datetime(
            year=date_time.year, month=date_time.month, day=date_time.day
        )
    elif round.up():
        rounded_date = datetime(
            year=date_time.year, month=date_time.month, day=date_time.day
        )
        rounded_date = datetime.fromtimestamp(
            rounded_date.timestamp() + seconds_per_day
        )
        while rounded_date.weekday() != 0:
            rounded_date = datetime.fromtimestamp(
                rounded_date.timestamp() + seconds_per_day
            )
        return rounded_date
    else:
        rounded_date = datetime(
            year=date_time.year, month=date_time.month, day=date_time.day
        )
        while rounded_date.weekday() != 0:
            rounded_date = datetime.fromtimestamp(
                rounded_date.timestamp() - seconds_per_day
            )
        return rounded_date


def is_week_scale_unit(scale_unit: int) -> bool:
    return scale_unit == WEEK_1


def round_by_months(
    date_time: datetime,
    months_in_scale_unit,
    round: Round
) -> datetime:
    months = ((date_time.year - 1) * 12) + (date_time.month - 1)
    if (
        round.up()
        and (
            date_time.day > 1
            or date_time.hour > 0
            or date_time.minute > 0
            or date_time.second > 0
        )
    ):
        months += 1

    multiples = months // months_in_scale_unit
    remainder = months % months_in_scale_unit
    if (remainder > 0) and round.up():
        multiples += 1

    rounded_months = multiples * months_in_scale_unit
    year = (rounded_months // 12) + 1
    month = (rounded_months % 12) + 1

    return datetime(year=year, month=month, day=1)


def is_month_scale_unit(scale_unit: int) -> bool:
    return scale_unit >= MONTH_1 and scale_unit <= MONTH_6


def get_months_in_scale_unit(scale_unit: int) -> int:
    return scale_unit - MONTH_PREFIX


def round_by_years(
    date_time: datetime,
    years_in_scale_unit,
    round: Round
) -> datetime:
    years = date_time.year
    if (
        round.up()
        and (
            date_time.month > 1
            or date_time.day > 1
            or date_time.hour > 0
            or date_time.minute > 0
            or date_time.second > 0
        )
    ):
        years += 1

    multiples = years // years_in_scale_unit
    remainder = years % years_in_scale_unit
    if (remainder > 0) and round.up():
        multiples += 1

    year = (multiples * years_in_scale_unit)
    return datetime(year=year, month=1, day=1)


def is_year_scale_unit(scale_unit: int) -> bool:
    return scale_unit >= YEAR_1 and scale_unit <= YEAR_1000


def get_years_in_scale_unit(scale_unit: int) -> int:
    return scale_unit - YEAR_PREFIX


def round_datetime(
        date_time: datetime,
        scale_unit: int,
        round: Round
) -> datetime:
    if is_week_scale_unit(scale_unit):
        return round_by_weeks(date_time, round)
    elif is_year_scale_unit(scale_unit):
        year_scale_unit = get_years_in_scale_unit(scale_unit)
        return round_by_years(date_time, year_scale_unit, round)
    elif is_month_scale_unit(scale_unit):
        month_scale_unit = get_months_in_scale_unit(scale_unit)
        return round_by_months(date_time, month_scale_unit, round)
    else:
        return round_by_seconds(date_time, scale_unit, round)


class DateTime(TimeUnit):
    def __init__(self, date_time: datetime):
        self.date_time = date_time

    def round_to_scale_unit(self, scale_unit: int, round: Round):
        self.date_time = round_datetime(self.date_time, scale_unit, round)

    def __str__(self) -> str:
        return str(self.date_time)

    def start_end_string(self, end: "DateTime") -> str:
        return f"{str(self)} to {str(end)}"
