import requests

def scan_websites() -> int:
    s = requests.Session()
    s.headers.update({
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    })
    #r = requests.get('https://www.nettiauto.com/mercedes-benz/sprinter?pto=4000&id_country[]=73')
    r = s.get('https://www.nettiauto.com', verify=False, allow_redirects=True)
    with open('file.html', 'w') as file:
        file.write(r.text)
    print(r)
    print(r.headers)
    print(r.status_code)
    return 1


if __name__ == '__main__':
    scan_websites()