import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.dgft.gov.in/CP/?opt=public-notice"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

table = soup.find("table", {"id": "metaTable"})
rows = table.find("tbody").find_all("tr")

data = []
for row in rows:
    cols = row.find_all("td")
    if not cols or len(cols) < 7:
        continue
    sl_no = cols[0].get_text(strip=True)
    number = cols[1].get_text(strip=True)
    year = cols[2].get_text(strip=True)
    description = cols[3].get_text(strip=True)
    date = cols[4].get_text(strip=True)
    # CRT DT is hidden, skip
    attachment_tag = cols[6].find("a")
    attachment = attachment_tag["href"] if attachment_tag else ""
    data.append({
        "Sl.No.": sl_no,
        "Number": number,
        "Year": year,
        "Description": description,
        "Date": date,
        "Attachment": attachment
    })

df = pd.DataFrame(data)
df[]
df.to_csv("dgft_public_notices.csv", index=False)  # Export to CSV
print("Exported to dgft_public_notices.csv")