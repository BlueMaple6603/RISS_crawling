from bs4 import BeautifulSoup as bs
import urllib.request
import get_ref as gr
import os

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

                re = gr.get_reference(paper_url)

                save_csv(csv_name, re)

def save_csv(csv_path, data):
    csv = csv_path.replace("/", "\\")

    if os.path.isfile(csv_path):
        data.to_csv(csv, mode='a', header=False, index=False)

    else:
        data.to_csv(csv, mode='w', header=True, index=False)
