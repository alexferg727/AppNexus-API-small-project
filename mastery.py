import requests
from bs4 import BeautifulSoup


def main(login_url):
    
    with requests.session() as client:

        login_page = client.get(login_url)

        soup = BeautifulSoup(login_page.content, 'html.parser')
        csrf_token = soup.find('input', {'name': 'logintoken'})['value']

        session_id = client.cookies['MoodleSession']

        print(session_id)

        payload = {
            'username': 'u6580169',
            'password': '',
            'logintoken': csrf_token,
            'MoodleSession': session_id
        }
        
        r1 = client.post(login_url, data=payload)

        print(r1.content)
        print(session_id)





if __name__ == '__main__':
    main('https://muicelearning.mahidol.ac.th/login/index.php')