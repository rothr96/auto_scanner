import getpass
from time import sleep
from typing import List
from random import randint

from auto_scanner.netti_auto import NettiAuto, NettiAutoError
from auto_scanner.email import send_email

NETTI_AUTO = NettiAuto()


def scrape_netti_auto() -> List[str]:
    try:
        return NETTI_AUTO.get_notifications()
    except NettiAutoError as e:
        print(e)
        return []


def scan_websites(passwd: str) -> None:
    while True:
        notifications = scrape_netti_auto()
        if notifications:
            send_email(passwd, notifications)
        sleep(randint(60, 5*60))


if __name__ == '__main__':
    passwd = getpass.getpass('Your email password: ')
    scan_websites(passwd)