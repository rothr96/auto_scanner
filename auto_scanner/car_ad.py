from dataclasses import dataclass


@dataclass
class CarAd:
    id: str
    make: str
    mileage: int
    model: str
    posted_by: str
    price: float
    vtype: str
    year: int
    link: str

    def as_new_ad(self) -> str:
        return (
            f"Uusi ilmoitus: {self.make} {self.model} {self.year}, "
            f"{self.mileage} km, {self.price:.2f} e, {self.posted_by}, {self.link}."
        )

    def as_removed_ad(self) -> str:
        return (
            f"Ilmoitus poistettu: {self.make} {self.model} {self.year}, "
            f"{self.mileage} km, {self.price:.2f} e, {self.posted_by}."
        )

    def as_price_reduced(self, previous_price: float) -> str:
        return (
            f"Hinta alennettu: {self.make} {self.model} {self.year}, "
            f"{self.mileage} km, uusi hinta {self.price:.2f} e ({previous_price:.2f}), "
            f"{self.posted_by}, {self.link}."
        )