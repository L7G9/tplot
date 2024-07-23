from timelines.pdf.time_unit import TimeUnit
from timelines.pdf.round import Round


class ScientificYear(TimeUnit):
    """Class representing an age time unit in years and months."""
    def __init__(self, fraction: float, multiplier: int):
        self.fraction = fraction
        self.multiplier = multiplier

    def fraction_string(self) -> str:
        """String describing the fraction."""
        return str(abs(self.fraction))

    def multiplier_string(self) -> str:
        """String describing the multiplier."""
        years = abs(self.multiplier)
        if years == 1000:
            return "thousand"
        elif years == 1000000:
            return "million"
        else:
            return "billion"

    def direction_string(self) -> str:
        """String describing if the event is in the past or future."""
        if self.fraction < 0:
            return "ago"
        elif self.fraction > 0:
            return "from now"
        else:
            return ""

    def __str__(self) -> str:
        return (
                    f"{self.fraction_string()} "
                    f"{self.multiplier_string()} years "
                    f"{self.direction_string()}"
                )

    def start_end_string(self, end: "ScientificYear") -> str:
        same_multiplier = self.multiplier == end.multiplier
        both_past = (self.fraction < 0.0) and (end.fraction < 0.0)
        both_future = (self.fraction >= 0.0) and (end.fraction >= 0.0)
        start_similar_to_end = same_multiplier and (both_past or both_future)

        if start_similar_to_end:
            return f"{self.fraction_string()} to {str(end)}"
        else:
            return f"{str(self)} to {str(end)}"

    def round(self, unit_size: int, round: Round):
        """Round fraction to nearest multiple of a given unit size."""

        multiples = int(self.years()) // unit_size
        remainder = int(self.years()) % unit_size

        if (remainder < 0) and round.down():
            multiples -= 1
        elif (remainder > 0) and round.up():
            multiples += 1

        self.fraction = (multiples * unit_size) / self.multiplier

    def change_multiplier(self, multiplier):
        """Update fraction to use given multiplier."""
        self.fraction = self.fraction * (self.multiplier / multiplier)
        self.multiplier = multiplier

    def years(self) -> float:
        return self.fraction * self.multiplier

    def __lt__(self, other) -> bool:
        return self.years() < other.years()

    def __le__(self, other) -> bool:
        return self.years() <= other.years()

    def __eq__(self, other) -> bool:
        return self.years() == other.years()

    def __ne__(self, other) -> bool:
        return self.years() != other.years()

    def __gt__(self, other) -> bool:
        return self.years() > other.years()

    def __ge__(self, other) -> bool:
        return self.years() >= other.years()
