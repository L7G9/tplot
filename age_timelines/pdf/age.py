from timelines.pdf.round import Round

MONTHS_PER_YEAR = 12


class Age:
    """Class representing an age time unit in years and months."""
    def __init__(self, years: int, months: int):
        self.years = years
        self.months = months

    def round_months(self, round: Round):
        """Round months to years."""
        years = self.months // MONTHS_PER_YEAR
        remainder = self.months % MONTHS_PER_YEAR
        if (remainder < 0) and round.down():
            years -= 1
        elif (remainder > 0) and round.up():
            years += 1

        self.years += years
        self.months = 0

    def round_years(self, year_unit_size: int, round: Round):
        """Round years to nearest multiple of a given unit size."""
        multiples = self.years // year_unit_size
        remainder = self.years % year_unit_size
        if (remainder < 0) and round.down():
            multiples -= 1
        elif (remainder > 0) and round.up():
            multiples += 1

        self.years = multiples * year_unit_size

    def __str__(self) -> str:
        if self.months == 0:
            return f"{self.years} Years"
        elif self.years == 0:
            return f"{self.months} Months"
        else:
            return f"{self.years} Years {self.months} Months"

    def __add__(self, other):
        return Age(self.years + other.years, self.months + other.months)

    def __sub__(self, other):
        return Age(self.years - other.years, self.months - other.months)

    def __iadd__(self, other):
        return Age(self.years + other.years, self.months + other.months)

    def __isub__(self, other):
        return Age(self.years - other.years, self.months - other.months)

    def total_months(self) -> int:
        return (self.years * MONTHS_PER_YEAR) + self.months

    def __lt__(self, other) -> bool:
        return self.total_months() < other.total_months()

    def __le__(self, other) -> bool:
        return self.total_months() <= other.total_months()

    def __eq__(self, other) -> bool:
        return self.total_months() == other.total_months()

    def __ne__(self, other) -> bool:
        return self.total_months() != other.total_months()

    def __gt__(self, other) -> bool:
        return self.total_months() > other.total_months()

    def __ge__(self, other) -> bool:
        return self.total_months() >= other.total_months()
