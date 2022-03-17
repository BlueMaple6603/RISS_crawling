import datetime
import getpass
import re
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup as bs
import urllib.request
import os
from tkinter import *

def get_url(page):
    url_before_page = "http://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&queryText=" \
                      "&strQuery=%EB%8F%99%EA%B5%B4&exQuery=dstitle%3A%EB%8F%99%EA%B5%B4%E2%97%88&exQueryText=%ED" \
                      "%95%99%EC%88%A0%EC%A7%80%EB%AA%85+%5B%EB%8F%99%EA%B5%B4%5D%40%40dstitle%3A%EB%8F%99%EA%B5%" \
                      "B4%E2%97%88&order=%2FDESC&onHanja=false&strSort=RANK&p_year1=&p_year2=&iStartCount="

    url_after_page = "&orderBy=&mat_type=&mat_subtype=&fulltext_kind=&t_gubun=&learning_type=&ccl_code=&inside_" \
                     "outside=&fric_yn=&image_yn=&gubun=&kdc=&ttsUseYn=&l_sub_code=&fsearchMethod=search&sflag=" \
                     "1&isFDetailSearch=N&pageNumber=1&resultKeyword=%EB%8F%99%EA%B5%B4&fsearchSort=&fsearchOrd" \
                     "er=&limiterList=&limiterListText=&facetList=&facetListText=&fsearchDB=&icate=re_a_kor&col" \
                     "Name=re_a_kor&pageScale=10&isTab=Y&regnm=&dorg_storage=&language=&language_code=&clickKey" \
                     "word=&relationKeyword=&query=%EB%8F%99%EA%B5%B4"

    url = url_before_page + page + url_after_page
    return url

def get_link(csv_name, page_num):
    for i in range(page_num):
        current_page = i * 10
        url = get_url(str(current_page))
        source_code_from_url = urllib.request.urlopen(url)
        soup = bs(source_code_from_url, 'lxml', from_encoding='utf-8')

        for j in range(10):
            try:
                paper_link = soup.select('li > div.cont > p.title > a')[j]['href']
            except IndexError:
                paper_link = 'no'
            else:
                paper_url = "http://riss.kr" + paper_link

                re = get_reference(paper_url)

                save_csv(csv_name, re)

def save_csv(csv_path, data):
    csv = csv_path.replace("/", "\\")

    if os.path.isfile(csv_path):
        data.to_csv(csv, mode='a', header=False, index=False)

    else:
        data.to_csv(csv, mode='w', header=True, index=False)


def get_reference(url):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver_path = os.path.join("/Users/권순율/PycharmProjects/pythonProject4", "chromedriver")
    driver = webdriver.Chrome(driver_path, options=options)
    driver.get(url)
    html = driver.page_source
    soup = bs(html, "html.parser")

    title = soup.find("h3", "title")
    title_txt = title.get_text("", strip=True).split("=")
    title_kor = re.sub("\n\b", "", str(title_txt[0]).strip())
    try:
        title_eng = str(title_txt[1]).strip()
    except IndexError:
        title_eng = "없음"

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
            "영문 제목": [title_eng],
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

def make_folder(folder_name):
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

if __name__ == "__main__":
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    user_name = getpass.getuser()
    folder_root = "/Users/권순율/PycharmProjects/pythonProject4"
    path = folder_root + now
    make_folder(path)

    def confirm():
        in_text1 = textbox1.get()
        in_text2 = textbox2.get()
        label3.configure(text=in_text1)
        label4.configure(text=in_text2)

        f_name = in_text1
        p_num = in_text2
        csv_path = path + "/" + f_name + ".csv"
        get_link(csv_path, int(p_num))

    window = Tk()
    window.title("RISS 검색기")
    window.geometry('300x200')
    window.resizable(False, False)

    name1 = StringVar()
    label1 = Label(window, text="csv파일명")
    label1.grid(column=0, row=0)
    textbox1 = Entry(window, width=40, textvariable=name1)
    textbox1.grid(column=0, row=1)

    name2 = StringVar()
    label2 = Label(window, text="페이지수")
    label2.grid(column=0, row=2)
    textbox2 = Entry(window, width=40, textvariable=name2)
    textbox2.grid(column=0, row=3)

    label3 = Label(window, text="", font=("돋음", 10))
    label3.grid(column=0, row=6)

    label4 = Label(window, text="", font=("돋음", 10))
    label4.grid(column=0, row=7)

    button = Button(window, text="확인", command=confirm)
    button.grid(column=0, row=4)

    window.mainloop()

