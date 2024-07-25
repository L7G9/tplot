from timelines.pdf.time_unit import TimeUnit
from timelines.pdf.round import Round


class HistoricalYear(TimeUnit):
    """Class representing an age time unit in years and months."""
    def __init__(self, year: int):
        self.year = year

    def __year_string(self) -> str:
        """"""
        return str(abs(self.year))

    def __bc_ad_string(self) -> str:
        """"""
        if self.year < 0:
            return "BC"
        else:
            return "AD"

    def __str__(self) -> str:
        if self.year == 0:
            return "BC/AD"
        else:
            return f"{self.__year_string()} {self.__bc_ad_string()}"

    def start_end_string(self, end: "HistoricalYear") -> str:
        """"""
        both_past = (self.year < 0) and (end.year < 0)
        both_future = (self.year > 0) and (end.year > 0)
        start_similar_to_end = both_past or both_future

        if start_similar_to_end:
            return f"{self.__year_string()} to {str(end)}"
        else:
            return f"{str(self)} to {str(end)}"

    def round(self, unit_size: int, round: Round):
        """Round year up or down to nearest multiple of unit size."""
        multiples = self.year // unit_size
        remainder = self.year % unit_size

        if (remainder < 0) and round.down():
            multiples -= 1
        elif (remainder > 0) and round.up():
            multiples += 1

        self.year = multiples * unit_size

    def __lt__(self, other) -> bool:
        return self.year < other.year

    def __le__(self, other) -> bool:
        return self.year <= other.year

    def __eq__(self, other) -> bool:
        return self.year == other.year

    def __ne__(self, other) -> bool:
        return self.year != other.year

    def __gt__(self, other) -> bool:
        return self.year > other.year

    def __ge__(self, other) -> bool:
        return self.year >= other.year
