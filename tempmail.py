import requests
from bs4 import BeautifulSoup
from datetime import datetime


class TemporaryMail:
    def __init__(self, domain: str):
        self.domain = domain
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Whale/3.19.166.16 Safari/537.36'}
        self.ruu_domains = ['ruu.kr', 'iralborz.bid', 'kumli.racing']
        self.temp_domains = ['cloud-mail.top', 'greencafe24.com', 'crepeau12.com', 'appzily.com', 'coffeetimer24.com',
                             'popcornfarm7.com', 'bestparadize.com', 'kjkszpjcompany.com', 'cashflow35.com', 'crossmailjet.com',
                             'kobrandly.com', 'blondemorkin.com', 'block521.com', 'best-john-boats.com', 'popcornfly.com', 'plancetose.com']

    def create_mail(self, id_: str) -> str:
        """Creates a new temporary email."""
        if self.domain in self.temp_domains:
            response = requests.post("https://api.internal.temp-mail.io/api/v3/email/new", json={"domain": self.domain, "name": id_},
                                     headers=self.headers)
            return response.json().get('token', None)

    def remove_mail(self, id_: str, token: str = None):
        """Removes a temporary email."""
        if self.domain in self.ruu_domains:
            mail_ids = self._fetch_ruu_mail_ids(id_)
            for mail_id in mail_ids:
                delete_url = f"http://ruu.kr/action.jsp?cmd=D&seq={mail_id}&to={id_}@{self.domain}"
                requests.get(delete_url, headers=self.headers)
        elif self.domain in self.temp_domains and token:
            delete_url = f"https://api.internal.temp-mail.io/api/v3/email/{id_}@{self.domain}"
            requests.delete(delete_url, json={"token": token}, headers=self.headers)

    def receive_mail(self, id_: str) -> list:
        """Fetches emails for the given ID."""
        if self.domain in self.ruu_domains:
            return self._fetch_ruu_emails(id_)
        elif self.domain in self.temp_domains:
            return self._fetch_temp_emails(id_)
        return []

    def _fetch_ruu_mail_ids(self, id_: str) -> list:
        resp = requests.get(f"http://ruu.kr/list.jsp?id={id_}&domain={self.domain}", headers=self.headers)
        return list(set([str(i).split("'")[1].split("'")[0] for i in BeautifulSoup(resp.text, 'html.parser').findAll('td') if "'" in str(i)]))

    def _fetch_ruu_emails(self, id_: str) -> list:
        resp = requests.get(f"http://ruu.kr/list.jsp?id={id_}&domain={self.domain}", headers=self.headers)
        soup = BeautifulSoup(resp.text, 'html.parser').findAll('td')
        mail_details = []
        for i in [soup[i:i + 4] for i in range(0, len(soup), 4)]:
            try:
                title = str(i[1]).split('>')[1].split("<")[0]
                mail_id = str(i[1]).split("'")[1].split("'")[0]
                mail_info = {'id': mail_id, 'title': title}
                mail_details.append(mail_info)
            except:
                pass
        emails = []
        for mail_detail in mail_details:
            resp = requests.get(f"http://ruu.kr/view.jsp?seq={mail_detail['id']}&to={id_}@{self.domain}", headers=self.headers)
            soup = BeautifulSoup(resp.text, 'html.parser')
            mail_info = soup.find('h2').text.split("/")
            email_address = mail_info[0].rstrip()
            date = datetime.strptime(mail_info[1].lstrip()[:-2], "%Y-%m-%d %H:%M:%S")
            content = soup.find('div', {"dir": "ltr"}).text if soup.find('div', {"dir": "ltr"}) else ""
            emails.append({'email': email_address, "title": mail_detail['title'], "date": date, "content_text": content, "content_html": soup.find('body')})
        return emails

    def _fetch_temp_emails(self, id_: str) -> list:
        resp = requests.get(f'https://api.internal.temp-mail.io/api/v3/email/{id_}@{self.domain}/messages', headers=self.headers).json()
        emails = []
        for mail in resp:
            title = mail['subject']
            email_address = mail['from'].split("<")[1].split(">")[0]
            date = datetime.strptime(mail['created_at'].split(".")[0], "%Y-%m-%dT%H:%M:%S")
            emails.append({'email': email_address, "title": title, "date": date, "content_text": mail["body_text"], "content_html": mail["body_html"]})
        return emails


if __name__ == "__main__":
    DOMAIN = ""  # Ex. ruu.kr
    ID = ""  # Ex. abcde12345

    temporary_mail_service = TemporaryMail(DOMAIN)

    # Mail creation feature only available for temp-mail.io
    # token = temporary_mail_service.create_mail(ID)

    print(temporary_mail_service.receive_mail(ID))

    # Removal only available for ruu.kr, but if you have a token from temp-mail.io, you can use it to remove the mail.
    # temporary_mail_service.remove_mail(ID, token)
