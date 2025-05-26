import requests
from bs4 import BeautifulSoup
import json

url = "https://www.freejobalert.com/government-jobs"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

jobs = []
# The main job table is the first table with class "job_table"
table = soup.find("table", class_="job_table")
if table:
    rows = table.find_all("tr")
    for row in rows[1:]:  # Skip header
        cols = row.find_all("td")
        if len(cols) >= 4:
            # Title and link
            title_elem = cols[1].find("a")
            title = title_elem.get_text(strip=True) if title_elem else cols[1].get_text(strip=True)
            link = title_elem["href"] if title_elem and "href" in title_elem.attrs else ""
            state = cols[2].get_text(strip=True) if cols[2] else "Other"
            jobs.append({
                "title": title,
                "link": link,
                "state": state,
                "source": "FreeJobAlert"
            })

with open("jobs.json", "w", encoding="utf-8") as f:
    json.dump(jobs, f, ensure_ascii=False, indent=2)
