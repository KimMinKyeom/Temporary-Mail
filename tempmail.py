import requests
from bs4 import BeautifulSoup
from datetime import datetime


class TemporaryMail:
    def __init__(self, domain):
        self.domain = domain
        self.ruu = ['ruu.kr', 'iralborz.bid', 'kumli.racing']
        self.temp = ['cloud-mail.top', 'greencafe24.com', 'crepeau12.com', 'appzily.com', 'coffeetimer24.com', 'popcornfarm7.com', 'bestparadize.com', 'kjkszpjcompany.com', 'cashflow35.com', 'crossmailjet.com', 'kobrandly.com', 'blondemorkin.com', 'block521.com', 'best-john-boats.com', 'popcornfly.com', 'plancetose.com']

    def create_mail(self, id_):
        if self.domain in self.temp:
            return requests.post("https://api.internal.temp-mail.io/api/v3/email/new", json={"domain": self.domain, "name": id_}).json()['token']

    def remove_mail(self, id_, token=None):
        if domain in self.ruu:
            resp = requests.get(f"http://ruu.kr/list.jsp?id={id_}&domain={self.domain}")
            mail_id = list(set([str(i).split("'")[1].split("'")[0] for i in BeautifulSoup(resp.text, 'html.parser').findAll('td') if "'" in str(i)]))
            for mail in mail_id:
                requests.get(f"http://ruu.kr/action.jsp?cmd=D&seq={mail}&to={id_}@{self.domain}")
        elif domain in self.temp:
            requests.delete(f"https://api.internal.temp-mail.io/api/v3/email/{id_}@{domain}", json={"token":token})

    def receive_mail(self, id_):
        result = []
        if self.domain in self.ruu:
            resp = requests.get(f"http://ruu.kr/list.jsp?id={id_}&domain={self.domain}")
            soup = BeautifulSoup(resp.text, 'html.parser').findAll('td')
            mail_ids = {}
            for i in [soup[i:i + 4] for i in range(0, len(soup), 4)]:
                try:
                    title = str(i[1]).split('>')[1].split("<")[0]
                    mail_id = str(i[1]).split("'")[1].split("'")[0]
                    mail_ids[mail_id] = title
                except:
                    pass
            for mail in mail_ids:
                resp = requests.get(f"http://ruu.kr/view.jsp?seq={mail}&to={id_}@{self.domain}")
                soup = BeautifulSoup(resp.text, 'html.parser')
                title = mail_ids[mail]
                mail_info = soup.find('h2').text.split("/")
                email = mail_info[0].rstrip()
                date = datetime.strptime(mail_info[1].lstrip()[:-2], "%Y-%m-%d %H:%M:%S")
                try:
                    content = soup.find('div', {"dir": "ltr"}).text
                except:
                    content = ""
                result.append({'email': email, "title": title, "date": date, "content_text": content, "content_html": soup.find('body')})
        elif self.domain in self.temp:
            resp = requests.get(f'https://api.internal.temp-mail.io/api/v3/email/{id_}@{self.domain}/messages').json()
            for mail in resp:
                title = mail['subject']
                email = mail['from'].split("<")[1].split(">")[0]
                date = datetime.strptime(mail['created_at'].split(".")[0], "%Y-%m-%dT%H:%M:%S")
                result.append({'email': email, "title": title, "date": date, "content_text": mail["body_text"], "content_html": mail["body_html"]})
        else:
            return False
        return result


if __name__ == "__main__":
    domain = ""  # Ex. ruu.kr
    name = ""  # Ex. abcde12345
    tm = TemporaryMail(domain)

    # token = tm.create_mail(name) # Only temp-mail.io
    print(tm.receive_mail(name))
    # tm.remove_mail(name, token) # Only ruu.kr can be used, but if you have a token of temp-mail.io, you can remove temp-mail.io.
