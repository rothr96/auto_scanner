import json
from typing import List

from auto_scanner.car_ad import CarAd


class CarScanner:
    def __init__(self, file_name) -> None:
        self.__file_name = file_name
    
    def write_ads(self, ads: List[CarAd]) -> None:
        with open(self.__file_name, 'w') as f:
            f.write(json.dumps([ad.__dict__ for ad in ads], indent=2))

    def read_ads(self) -> List[CarAd]:
        try:
            with open(self.__file_name, 'r') as f:
                listings = json.loads(f.read())
                return [CarAd(**ad) for ad in listings]
        except FileNotFoundError:
            return []

    @staticmethod
    def resolve_diff(previous_ads: List[CarAd], current_ads: List[CarAd]) -> List[str]:
        previous_lookup = {ad.id: ad for ad in previous_ads}
        current_lookup = {ad.id: ad for ad in current_ads}
        new_ads = [
            ad.as_new_ad()
            for ad in current_ads
            if ad.id not in previous_lookup
        ]
        removed_ads = [
            ad.as_removed_ad()
            for ad in previous_ads
            if ad.id not in current_lookup
        ]
        price_reduced = [
            ad.as_price_reduced(previous_lookup[ad.id].price)
            for ad in current_ads
            if ad.id in previous_lookup and previous_lookup[ad.id].price > ad.price
        ]
        return new_ads + price_reduced + removed_ads
