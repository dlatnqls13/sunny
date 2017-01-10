import difflib
import requests
import argparse
from bs4 import BeautifulSoup


class PlagiarismCheck(object):
    def __init__(self, u1, u2):
        self.u1 = u1
        self.u2 = u2

    def html_parser (self, url):
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'lxml')
        soup.find_all('div', attrs={'id': 'articleText'})
        article = soup.find_all('div', attrs={'id': 'articleText'})
        type(article[0])

        return article[0].text

    def compare (self, a, b):
        seq = difflib.SequenceMatcher()
        seq.set_seqs(a.lower(), b.lower())
        return seq.ratio() * 100

    def main (self):
        aa = self.html_parser(self.u1)
        bb = self.html_parser(self.u2)
        check = self.compare(aa, bb)
        self.send_simple_message(check)
        # self.html_parser()

    def send_simple_message (self, check):
        return requests.post(
            "https://api.mailgun.net/v3/sandbox7bb8c62214184e15a2985162e7422c1c.mailgun.org/messages",
            auth=("api", "key-074b8af39fa5525dcf9df0bc8116ae82"),
            data={"from": "Mailgun Sandbox <postmaster@sandbox7bb8c62214184e15a2985162e7422c1c.mailgun.org>",
                  "to": "sunny <believe11043@gmail.com>",
                  "subject": "Hello sunny",
                  "text": '{}과 {}의 기사의 유사도 비교 결과: {} %' .format(self.u1, self.u2, check)}
        )

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u1', type=str, help='INPUT URL(start with http://)', required=True)
    parser.add_argument('-u2', type=str, help='INPUT URL(start with http://)', required=True)
    args = parser.parse_args()
    print(args.u1, args.u2)

    pc = PlagiarismCheck(u1=args.u1, u2=args.u2)
    pc.main()
