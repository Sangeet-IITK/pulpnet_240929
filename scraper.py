import requests
from bs4 import BeautifulSoup, Tag
import re
import csv

URL = "https://www.iitk.ac.in/aero/all-disciplines"
response = requests.get(URL)
soup = BeautifulSoup(response.content, "lxml")

faculty_data = []

for p in soup.find_all("p"):
    if isinstance(p, Tag):
        a = p.find("a", class_="wtk-links")
        if a:
            name = a.get_text(strip=True)
            title = p.get_text(separator=" ", strip=True)
            title = title.replace(name, "").strip().strip(",")
            email = ""
            phone = ""
            research_interests = ""
            next_tag = p.find_next_sibling()
            for _ in range(5):
                if not next_tag:
                    break
                if isinstance(next_tag, Tag):
                    text = next_tag.get_text(separator=" ", strip=True)
                    email_match = re.search(r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", text)
                    if email_match:
                        email = email_match.group(1)
                    phone_match = re.search(r"\+91[-\d ()]+", text)
                    if phone_match:
                        phone = phone_match.group(0)
                    if "Research Interests" in text:
                        research_interests = text.split(":", 1)[-1].strip()
                next_tag = next_tag.find_next_sibling()
            faculty_data.append({
                "name": name,
                "title": title,
                "email": email,
                "phone": phone,
                "research_interests": research_interests
            })

with open("iitk_data", "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "title", "email", "phone", "research_interests"])
    writer.writeheader()
    writer.writerows(faculty_data)

print(f"Scraped {len(faculty_data)} faculty entries and saved to iitk_aero_faculty.csv") 