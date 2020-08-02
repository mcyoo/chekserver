from urllib.request import Request, urlopen
from urllib import parse
import hashlib
from bs4 import BeautifulSoup


def make_md5(page):
    soup = BeautifulSoup(page, "html.parser")
    body = soup.find("body").text
    print(body)
    if type(body) != bytes:
        body = body.encode("utf-8")
    md5 = hashlib.md5(body).hexdigest()
    return md5


def get_title(page):
    soup = BeautifulSoup(page, "html.parser")
    title = soup.find("title").text
    return title.strip()


url = "http://2ditor.com/product/thalassa-m-%ED%83%88%EB%9D%BC%EC%82%ACm-%EB%B9%85-%ED%8E%B8%EA%B4%91-%EC%84%A0%EA%B8%80%EB%9D%BC%EC%8A%A4/533/category/131/display/1/"
print(url.encode("utf8"))
url = parse.quote(url.encode("utf8"), "/:?&=")

print(url)
request = Request(
    url,
    headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
    },  # Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36
    # Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25
)  # UA가 없으면 403 에러 발생
response = urlopen(request).read()
# print(response)
print(get_title(response))
print(make_md5(response))
# print(response)

