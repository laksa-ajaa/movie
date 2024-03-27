import requests
from bs4 import BeautifulSoup

url = "https://www.imdb.com/title/tt0111161/?ref_=chttp_t_1"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

data = requests.get(url, headers=headers)
soup = BeautifulSoup(data.text, "html.parser")


og_image = soup.select_one('meta[property="og:image"]')
og_title = soup.select_one('meta[property="og:title"]')
og_description = soup.select_one('meta[name="description"]')

title = og_title['content'].split('(')[0].strip()
image = og_image['content']
desc = og_description['content']

print(title)
print(image)
print(desc)
