from extractors.wwwr import extract_wwr_jobs
from extractors.worknet import extract_worknet_jobs

keyword = input("What do you want to search for?")

wwwr = extract_wwr_jobs(keyword)
worknet = extract_worknet_jobs(keyword)
jobs = wwwr + worknet

file = open(f"{keyword}.csv", "w")
file.write("Site,Compnay,BusinessInformation,Experience,Education,LocalName,Day,Deadline,Link\n")

for job in jobs:
    file.write(f"{job['site']},{job['title']},{job['businessinformation']},{job['experience']},{job['education']},{job['localname']},{job['day']},{job['deadline']},{job['link']}\n")

file.close()