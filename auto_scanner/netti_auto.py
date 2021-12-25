

import cloudscraper
from cloudscraper.exceptions import CloudflareChallengeError
from bs4 import BeautifulSoup
from bs4.element import PageElement
from auto_scanner.car_scanner import CarScanner
from typing import List
import json
from requests import Response

from auto_scanner.car_ad import CarAd

NETTI_AUTO_DATA_FILE_NAME = 'data/netti-auto-data.json'
NETTI_AUTO_CONFIG_FILE_NAME = 'config/netti-auto-config.json'


class NettiAutoError(Exception):
    pass


class NettiAuto:
    def __init__(self):
        self.__car_scanner = CarScanner(NETTI_AUTO_DATA_FILE_NAME)
        with open(NETTI_AUTO_CONFIG_FILE_NAME, 'r') as f:
            self.__urls = json.loads(f.read())
        self.__scraper = cloudscraper.create_scraper()

    @staticmethod
    def __to_car_add(link: PageElement) -> CarAd:
        return CarAd(
            id=link.attrs['data-id'],
            make=link.attrs['data-make'],
            mileage=int(link.attrs['data-mileage']),
            model=link.attrs['data-model'],
            posted_by=link.attrs['data-postedby'],
            price=float(link.attrs['data-price']),
            vtype=link.attrs['data-vtype'],
            year=int(link.attrs['data-year']),
            link=link.attrs['href'],
        )

    def __get(self, url: str) -> Response:
        try:
            response = self.__scraper.get(url, headers={
                'user-agent': 'Mozilla/5.0'
            })
            print(f"GET {response.status_code}: {url}")
            return response
        except CloudflareChallengeError as e:
            raise NettiAutoError(f"{e}")

    def get_notifications(self) -> List[str]:
        current_ads = []
        for url in self.__urls:
            navigation_response = self.__get(url)
            parsed_navigation = BeautifulSoup(navigation_response.text, 'html.parser')
            page_links = {
                link.attrs['href']
                for link in parsed_navigation.find_all(class_="pageNavigation")
            }
            for page_link in page_links:
                page_response = self.__get(page_link)
                parsed_page = BeautifulSoup(page_response.text, 'html.parser')
                current_ads.extend([
                    self.__to_car_add(link)
                    for link in parsed_page.find_all(class_="tricky_link")
                    if 'data-id' in link.attrs
                ])
        previous_ads = self.__car_scanner.read_ads()
        self.__car_scanner.write_ads(current_ads)
        return self.__car_scanner.resolve_diff(previous_ads, current_ads)
