from rest_framework import serializers
from .models import Domain
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import hashlib
from urllib import parse

user_agent = "Mozilla/5.0 (Linux; U; Android 4.0.3; de-ch; HTC Sensation Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("title", "url", "change", "filterling")
        model = Domain
        read_only_fields = ("title", "change", "filterling")

    def make_md5(self, page):
        soup = BeautifulSoup(page, "html.parser")
        body = soup.find("body").text
        if type(body) != bytes:
            body = body.encode("utf-8")
        md5 = hashlib.md5(body).hexdigest()
        return md5

    def get_title(self, page):
        soup = BeautifulSoup(page, "html.parser")
        content = soup.find("title").text
        return content.strip()

    def append_data(self, url):
        try:
            url = parse.quote(url.encode("utf8"), "/:?&=")
            request = Request(url, headers={"User-Agent": user_agent},)
            response = urlopen(request)
            page = response.read()
            return self.get_title(page), self.make_md5(page)
        except Exception as e:
            print("error log DomainSerializer append_data : ", e)
            return "페이지 에러", ""

    def get_filterling_page(self, url, filterling):
        try:
            url = parse.quote(url.encode("utf8"), "/:?&=")
            request = Request(url, headers={"User-Agent": user_agent},)
            response = urlopen(request)
            page = response.read()

            soup = BeautifulSoup(page, "html.parser")

            content = soup.find("title").text
            title = content.strip()

            node_name, class_name = filterling.split(",")
            body = soup.find(node_name.lower(), {"class": class_name})

            print(body)
            if type(body) != bytes:
                body = body.encode("utf-8")
            md5 = hashlib.md5(body).hexdigest()
            return title, md5

        except Exception as e:
            print("error log DomainSerializer get_filterling_page : ", e)
            return None

    def validate_url(self, value):
        if value[-1] != "/":
            value = value + "/"
        return value

    def update(self, instance, validated_data):
        filterling = self.context.get("filterling")
        url = instance.url

        instance.filterling = filterling
        instance.change = False

        if filterling != "":
            print(filterling)
            title_md5 = self.get_filterling_page(url, filterling)
            if title_md5 is None:
                instance.title = "페이지 에러"
                instance.html = ""
            else:
                instance.title = title_md5[0]
                instance.html = title_md5[1]
        else:
            title, md5 = self.append_data(url)
            instance.title = title
            instance.html = md5

        instance.save()
        return instance

    def create(self, validated_data):
        token = self.context.get("token")
        url = validated_data.get("url")
        title, md5 = self.append_data(url)
        # print(url, title, md5)
        domain = Domain.objects.create(
            **validated_data, token=token, title=title, html=md5
        )
        return domain
