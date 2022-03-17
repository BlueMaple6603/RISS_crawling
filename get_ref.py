from bs4 import BeautifulSoup as bs
import re
from selenium import webdriver
import pandas as pd
import os


def get_reference(url):
    driver_path = os.path.join("/Users/권순율/PycharmProjects/pythonProject4", "chromedriver")
    driver = webdriver.Chrome(driver_path, options=webdriver.ChromeOptions().add_argument("headless"))
    driver.get(url)
    html = driver.page_source
    soup = bs(html, "html.parser")

    title = soup.find("h3", "title")
    title_txt = title.get_text("", strip=True).split("=")
    title_kor = re.sub("\n\b", "", str(title_txt[0]).strip())
    #title_eng = str(title_txt[1]).strip()

    txt_box = []
    for text in soup.find_all("div", "text"):
        txt = text.get_text("", strip=True)
        txt_box.append(txt)

    try:
        txt_kor = txt_box[1]
    except IndexError:
        txt_kor = "없음"

    try:
        txt_eng = txt_box[3]
    except IndexError:
        txt_eng = "없음"

    detail_box = []
    detail_info = soup.select(
        "#soptionview > div > div.thesisInfo > div.infoDetail.on > div.infoDetailL > ul > li > div > p")

    for detail in detail_info:
        detail_content = detail.get_text("", strip=True)
        detail_wrap = []
        detail_wrap.append(detail_content)

        detail_box.append(detail_wrap)

    author = ",".join(detail_box[0])
    year = ",".join(detail_box[4])
    book = ("".join(detail_box[2] + detail_box[3]).replace("\n", "").replace("\t", "").replace(" ", "")
            + " p." + "".join(detail_box[-2]))
    keyword = ",".join(detail_box[6])

    reference_data = pd.DataFrame(
        {
            "저자": [author],
            "국문 제목": [title_kor],
            #"영문 제목": [title_eng],
            "발행년도": [year],
            "수록지": [book],
            "핵심어": [keyword],
            "국문 요약": [txt_kor],
            "영문 요약": [txt_eng],
            "링크": [url],
        }
    )

    driver.close()

    return reference_data