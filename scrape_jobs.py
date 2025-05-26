import requests
from bs4 import BeautifulSoup
import json

url = "https://www.freejobalert.com/government-jobs"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

jobs = []
table = soup.find("table", class_="job_table")
if table:
    rows = table.find_all("tr")
    for row in rows[1:]:
        cols = row.find_all("td")
        if len(cols) >= 4:
            title = cols[1].get_text(strip=True)
            link = cols[1].find("a")["href"] if cols[1].find("a") else ""
            state = cols[2].get_text(strip=True) if cols[2] else "Other"
            job = {
                "title": title,
                "link": link,
                "state": state,
                "source": "FreeJobAlert"
            }
            jobs.append(job)

with open("jobs.json", "w", encoding="utf-8") as f:
    json.dump(jobs, f, ensure_ascii=False, indent=2)