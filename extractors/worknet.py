from requests import get
from bs4 import BeautifulSoup

def get_page_count(keyword):
    base_url = "https://www.work.go.kr/wnSearch/unifSrch.do?regDateStdt=&regDateEndt=&colName=tb_workinfo&srchDateSelected=all&sortField=RANK&sortOrderBy=DESC&searchDateInfo=&temp=&pageIndex=1&tabName=tb_workinfo&dtlSearch=&query="
    response = get(f"{base_url}{keyword}")
    if response.status_code != 200:
        print(f"{response}\n### Can't request website ###")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        pagination = soup.find('nav', class_='pagination')
        if pagination == None:
            return 1
        pages = pagination.find_all('a')
        count = len(pages)
        if count >= 10:
            return 10
        else:
            return count+1
def extract_worknet_jobs(keyword):
    pages = get_page_count(keyword)
    print("Worknet site Found", pages, "pages")
    results = []
    for page in range(pages):
        base_url = "https://www.work.go.kr/wnSearch/unifSrch.do?regDateStdt=&regDateEndt=&colName=tb_workinfo&srchDateSelected=all&sortField=RANK&sortOrderBy=DESC&searchDateInfo=&temp="
        final_url = f"{base_url}&pageIndex={page+1}&query={keyword}"
        print("Requseting", final_url)
        response = get(final_url)
        if response.status_code != 200:
            print(f"{response}\n### Can't request website ###")
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            jobs = soup.find_all('div', class_="result-recruit-list")   # 직업 정보(덩어리)가 있는 큰 틀(섹션) 찾기
            for job_section in jobs:
                job_posts = job_section.find_all('div', class_='top')
                for post in job_posts:
                    anchors = post.find_all('a')
                    anchor = anchors[0]
                    link = anchor['href']

                    day = post.find('p', class_='d-day')
                    if day == None:
                        day = "None"  
                    else:
                        day = day.string

                    date = post.find('p', class_='date')
                    company = post.find('span')

                    job_data = {
                        'site' : "Worknet",
                        'title' : company.string,
                        'businessinformation' : "None",
                        'experience' : "None",
                        'education' : "None",
                        'localname' : "None",
                        'day' : day.replace(",", " "),
                        'deadline' : date.string.replace(",", " "),
                        'link' : f"https://www.work.go.kr/{link}"
                    }
                    results.append(job_data)
    return results