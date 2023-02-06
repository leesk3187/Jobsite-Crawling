from requests import get
from bs4 import BeautifulSoup

def get_page_count(keyword):
    base_url = "https://www.jobkorea.co.kr/Search/?stext="
    response = get(f"{base_url}{keyword}")
    if response.status_code != 200:
        print(f"{response}\n### Can't request website ###")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        pagination = soup.find('div', class_='tplPagination newVer wide')
        if pagination == None:  #페이지가 하나도 없을 시에는 1로 반환
            return 1
        pages = pagination.find_all('li')
        count = len(pages)
        if count >= 10:
            return 10
        else:
            return count
def extract_wwr_jobs(keyword):
    pages = get_page_count(keyword)
    print("Jonkorea site Found", pages, "pasges")
    results = []
    for page in range(pages):       # 페이지 수 만큼 반복 
        base_url = "https://www.jobkorea.co.kr/Search"
        final_url = f"{base_url}/?stext={keyword}&Page_No={page+1}"
        print("Requseting", final_url)
        response = get(final_url)
        if response.status_code != 200:
            print(f"{response}\n### Can't request website ###")
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            jobs = soup.find_all('div', class_="list-default")   # 직업 정보(덩어리)가 있는 큰 틀(섹션) 찾기
            if len(jobs) >= 2 :
                jobs.pop(-1)        # list_default가 두개 있기 떄문에 필요 없는 것 삭제
            for job_section in jobs:    
                job_posts = job_section.find_all("div", class_='post') # 조금 더 작은 범위로 들어가기
                for post in job_posts:
                    anchors = post.find_all('a')    # 링크 저장

                    anchor = anchors[0]     # 기업 이름 title을 얻기 위함.
                    link = anchor['href']   # anchors[1]하고 링크는 동일.
                    company = anchor['title']   # 기업 이름

                    workname = anchors[1]   # 업무 내용을 가져온다. 39행 BusinessInformation을 얻기 위함.
                    work = workname['title']    # 업무 내용
                    
                    #find_all은 리스트로 저장하고, find는 값만 저장한다.
                    experience = post.find('span', class_='exp')    #경력
                    education = post.find('span', class_='edu')     #학력
                    localname = post.find('span', class_='loc long')    #지역
                    deadline = post.find('span', class_='date')     #마감일

                    if education == None:       # 학력 정보가 없을 경우에는 다른 값으로 저장
                        education = "No problem"    # No problem으로 저장
                    else:
                        education = education.string

                    job_data = {
                        'site' : "Jobkorea",
                        'title' : company,
                        'businessinformation' : work.replace(",", " "),
                        'experience' : experience.string.replace(",", " "),
                        'education' : education.replace(",", " "),
                        'localname' : localname.string.replace(",", " "),
                        'day' : "",
                        'deadline' : deadline.string.replace(",", " "),
                        'link' : f"https://www.jobkorea.co.kr/{link}"
                    }
                    results.append(job_data)    # 바깥에 리스트르 값을 저장한다.
    return results