import re
from dataclasses import dataclass, field
from enum import Enum


class ArticleType(Enum):
    standard = 1
    newly_built = 2


class OwnershipTyp(Enum):
    self_owned = 1
    shared = 2


class ApartmentType(Enum):
    regular = 1


@dataclass
class ArticlePreScraping:
    url: str

    full_url: str = field(init=False)
    id: str = field(init=False)
    type: ArticleType = field(init=False)

    def __post_init__(self):
        finn_code, *_ = re.search(r"finnkode=([0-9]*)", self.url).groups()
        self.id = finn_code

        base_url = "https://www.finn.no"

        if self.url.startswith("/eiendom/nybygg/prosjekt"):
            self.full_url = f"{base_url}/eiendom/nybygg/prosjekt?finnkode={self.id}"
            self.type = ArticleType.newly_built
        elif self.url.startswith("/realestate/homes/"):
            self.type = ArticleType.standard
            self.full_url = f"{base_url}/realestate/homes/ad.html?finnkode={self.id}"
        else:
            print(f"Unknown article type {self.url}")


@dataclass
class Housing:
    primary_area: int
    usable_area: int
    brutto_area: int
    #
    shared_area: int

    monthly_fees: int

    shared_debt: int
    shared_capital: int
    shared_worth: int
    fees: int
    total_price: int

    # apartment_type: ApartmentType
    # ownership_type: OwnershipType

    bedrooms: int
    built_in_year: int
    floor: int

    has_balcony: bool
    has_fireplace: bool
    is_child_friendly: bool
    is_calm: bool
    has_cable_tv: bool
    is_modern: bool
    is_central: bool
    has_air_condition: bool
    has_public_water_sewage: bool
    has_alarm: bool
    has_view: bool
    has_janitorial_services: bool
    has_common_dry_cleaning: bool
    has_internet: bool

    estimated_price: int
    address: str
