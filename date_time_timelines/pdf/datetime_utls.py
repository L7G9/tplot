"""Contains utility functions using datetime.

Functions:
    round_by_seconds
    round_by_weeks
    round_by_months
    round_by_years
    get_start_of_month
    get_start_of_next_month
    seconds_between
    get_month_completion
"""


from datetime import datetime

from timelines.pdf.round import Round


def round_by_seconds(
    date_time: datetime,
    seconds_per_scale_unit,
    round: Round
) -> datetime:
    """Round a datetime instance by seconds.

    e.g. date_time has 24353237 seconds in it's timestamp and
    seconds_per_scale_unit is 5.  If round is down, the return datetime will
    have 24353235 seconds in it's timestamp.  If round is up, the return
    datetime will have 24353240 seconds in it's timestamp.

    Args:
        date_time: A datetime instance to be rounded.
        seconds_per_scale_unit: An int equal number of seconds to round to.
        round: A Round instance
    Returns:
        A datetime containing the rounded datetime argument.
    """
    seconds = int(date_time.timestamp())
    multiples = seconds // seconds_per_scale_unit
    remainder = seconds % seconds_per_scale_unit
    if (remainder > 0) and round.up():
        multiples += 1

    return datetime.fromtimestamp(multiples * seconds_per_scale_unit)


def round_by_weeks(
    date_time: datetime,
    round: Round
) -> datetime:
    """Round a datetime by week.

    e.g. date_time is 2000/01/10, a Wednesday.  If round is down, the return
    datetime will be 2000/01/7, the preceding Monday.  If round is up, the
    return datetime will be 2000/01/14, the next Monday.

    Args:
        date_time: A datetime instance to be rounded.
        round: A Round instance
    Returns:
        A datetime containing the rounded datetime argument.
    """
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


def round_by_months(
    date_time: datetime,
    months_per_scale_unit,
    round: Round
) -> datetime:
    """Round a datetime instance by months.

    e.g. date_time is 2000/02/15 and  months_per_scale_unit is 3.  If round is
    down, the return datetime will be 2000/01/01.  If round is up, the return
    datetime will be 2000/04/01.

    Args:
        date_time: A datetime instance to be rounded.
        months_per_scale_unit: An int equal number of months to round to.
        round: A Round instance
    Returns:
        A datetime containing the rounded datetime argument.
    """
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

    multiples = months // months_per_scale_unit
    remainder = months % months_per_scale_unit
    if (remainder > 0) and round.up():
        multiples += 1

    rounded_months = multiples * months_per_scale_unit
    year = (rounded_months // 12) + 1
    month = (rounded_months % 12) + 1

    return datetime(year=year, month=month, day=1)


def round_by_years(
    date_time: datetime,
    years_per_scale_unit,
    round: Round
) -> datetime:
    """Round a datetime instance by years.

    e.g. date_time is 2005/02/15 and  years_per_scale_unit is 10.  If round is
    down, the return datetime will be 2000/01/01.  If round is up, the return
    datetime will be 2010/01/01.

    Args:
        date_time: A datetime instance to be rounded.
        years_per_scale_unit: An int equal number of years to round to.
        round: A Round instance
    Returns:
        A datetime containing the rounded datetime argument.
    """
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

    multiples = years // years_per_scale_unit
    remainder = years % years_per_scale_unit
    if (remainder > 0) and round.up():
        multiples += 1

    year = (multiples * years_per_scale_unit)
    return datetime(year=year, month=1, day=1)


def get_start_of_month(date_time: datetime) -> datetime:
    """Get the date of the start of the month.

    e.g. date_time is 2000/03/15.  The return datetime will be 2000/03/01.

    Args:
        date_time: A datetime instance to get the start of the month from.

    Returns:
        A datetime containing the start of the month.
    """
    return datetime(
        year=date_time.year,
        month=date_time.month,
        day=1
    )


def get_start_of_next_month(date_time: datetime) -> datetime:
    """Get the date of the start of the next month.

    e.g. date_time is 2000/03/15.  The return datetime will be 2000/04/01.

    Args:
        date_time: A datetime instance to get the start of the next month
        from.

    Returns:
        A datetime containing the start of the next month.
    """
    if date_time.month < 12:
        return datetime(
            year=date_time.year,
            month=date_time.month + 1,
            day=1
        )
    else:
        return datetime(
            year=date_time.year + 1,
            month=1,
            day=1
        )


def seconds_between(from_date: datetime, to_date: datetime) -> int:
    """Get number of seconds between 2 datetime instances.

    Args:
        from_date: A datetime instance.
        to_date: A datetime instance.

    Returns:
        An int equal to the number of seconds between from_date and to_date.
    """
    return int(to_date.timestamp()) - int(from_date.timestamp())


def get_month_completion(date_time: datetime) -> float:
    """Get how much of the current month in date_time has been completed as a
    fraction.

    e.g. date_time is 2000/11/16 (a month with 30 days).  The return fraction
    will be 0.5 because exactly half the month has been completed.

    Args:
        date_time: A datetime instance.

    Returns:
        An float equal to the fraction of the month in date_time completed.

    """
    month_start = get_start_of_month(date_time)
    next_month_start = get_start_of_next_month(date_time)
    seconds_in_month = seconds_between(month_start, next_month_start)
    seconds_from_start_of_month = seconds_between(month_start, date_time)

    return (
        seconds_from_start_of_month
        / seconds_in_month
    )
