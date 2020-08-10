import os
import hashlib
import asyncio
import time
from firebase_admin import messaging
from firebase_admin import credentials
from firebase_admin import initialize_app
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib import parse

user_agent = "Mozilla/5.0 (Linux; U; Android 4.0.3; de-ch; HTC Sensation Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()
from users.models import User
from domains.models import Domain

cred = credentials.Certificate("fir-test-d20b3-firebase-adminsdk-u3j7c-f95f9b1e7d.json")
initialize_app(cred)


def send_to_app(token, title, url):
    message = messaging.Message(
        apns=messaging.APNSConfig(
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    alert=messaging.ApsAlert(title=title, body="사이트 변경"),
                    sound=messaging.CriticalSound(name="default",),
                    badge=1,
                ),
            ),
        ),
        android=messaging.AndroidConfig(
            notification=messaging.AndroidNotification(
                title=title,
                body="사이트 변경",
                default_sound=True,
                default_light_settings=True,
                visibility="public",
                priority="high",
                # notification_count=1,
            )
        ),
        token=token,
    )
    try:
        response = messaging.send(message)
        print(
            time.strftime("%c : ", time.localtime(time.time())),
            "Successfully sent message:",
            response,
        )
        return True
    except Exception as e:
        print(
            time.strftime("%c : ", time.localtime(time.time())),
            "send message but fail you need delete token",
            e,
        )
        print(token)

    return False


def delete_user(token):
    try:
        user = User.objects.get(token=token)
        print(
            time.strftime("%c : ", time.localtime(time.time())),
            "delete_user : token is invaild i will delete:",
            user,
        )
        user.delete()
    except Exception as e:
        print(
            time.strftime("%c : ", time.localtime(time.time())),
            "delete_user(token) error",
            e,
        )


def get_false_list():
    not_change_list = []
    try:
        check_domain = Domain.objects.filter(change=False)
        for domain in check_domain:
            not_change_list.append(domain)
    except Exception as e:
        print(
            time.strftime("%c : ", time.localtime(time.time())),
            "get_false_list() error",
            e,
        )

    print(time.strftime("%c : ", time.localtime(time.time())), not_change_list)
    return not_change_list


getData_DB = get_false_list()
getData_DB_Len = len(getData_DB)


def make_md5(page):
    soup = BeautifulSoup(page, "html.parser")
    body = soup.find("body").text
    if type(body) != bytes:
        body = body.encode("utf-8")
    md5 = hashlib.md5(body).hexdigest()
    return md5


def make_md5_filterling(page, filterling):
    soup = BeautifulSoup(page, "html.parser")
    try:
        node_name, class_name = filterling.split(",")
        body = soup.find(node_name.lower(), {"class": class_name})

        if type(body) != bytes:
            body = body.encode("utf-8")
        md5 = hashlib.md5(body).hexdigest()
    except:
        md5 = "no element"
    return md5


def get_title(page):
    soup = BeautifulSoup(page, "html.parser")
    title = soup.find("title").text
    return title.strip()


async def fetch(url_filter):
    try:
        url = url_filter[0]
        filterling = url_filter[1]
        print(url)
        print(filterling)
        url = parse.quote(url.encode("utf8"), "/:?&=")
        request = Request(url, headers={"User-Agent": user_agent},)  # UA가 없으면 403 에러 발생
        response = await loop.run_in_executor(
            None, urlopen, request
        )  # run_in_executor 사용
        page = await loop.run_in_executor(None, response.read)
        title = await loop.run_in_executor(None, get_title, page)
        if filterling == "" or filterling is None:
            md5 = await loop.run_in_executor(None, make_md5, page)
        else:
            md5 = await loop.run_in_executor(
                None, make_md5_filterling, page, filterling
            )

    except Exception as e:
        print(
            time.strftime("%c : ", time.localtime(time.time())),
            "async def fetch(url): error",
            e,
        )
        return None
    return title, md5


async def main():
    url_filter_list = [(domain.url, domain.filterling) for domain in getData_DB]
    futures = [
        asyncio.ensure_future(fetch(url_filter)) for url_filter in url_filter_list
    ]
    # 태스크(퓨처) 객체를 리스트로 만듦
    result = await asyncio.gather(*futures)  # 결과를 한꺼번에 가져옴
    return result
    # diff_md5(result)


# new_data = [(title,md5),(title,md5),....]
def main_checkChange(new_data):
    if getData_DB_Len == len(new_data):
        for i in range(getData_DB_Len):
            if new_data[i] is None:  # request fail
                change_DB(i, None)
            else:
                domain_title = getData_DB[i].title
                domain_url = getData_DB[i].url
                domain_token = getData_DB[i].token.token
                domain_html = getData_DB[i].html
                # print(domain_title, domain_url, domain_token, domain_html)
                if new_data[i][1] != domain_html:
                    print(
                        time.strftime("%c : ", time.localtime(time.time())),
                        domain_title,
                        "is chage!!",
                    )
                    send_to_app(domain_token, domain_title, domain_url)
                    change_DB(i, new_data[i])


def change_DB(index, new_data):
    obj_Domain = getData_DB[index]
    if new_data is not None:
        obj_Domain.title = new_data[0]
        obj_Domain.html = new_data[1]
        obj_Domain.change = True
    else:
        obj_Domain.title = "페이지 에러"
        obj_Domain.html = ""
        obj_Domain.change = False
    obj_Domain.save()


if __name__ == "__main__":
    try:
        begin = time.time()
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(main())
        loop.close()
        end = time.time()

        print("request get 실행 시간: {0:.3f}초".format(end - begin))

        begin = time.time()
        main_checkChange(result)
        end = time.time()

        print("change DB 실행 시간: {0:.3f}초".format(end - begin))

    except Exception as e:
        print(time.strftime("%c : ", time.localtime(time.time())), "__main__ error", e)

