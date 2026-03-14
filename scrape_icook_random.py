# file: scrape_icook_random.py
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random

# 頁面 URLs
urls = [
    f"https://icook.tw/search/%E5%81%A5%E8%BA%AB%E9%A4%90/?page={i}"
    for i in range(1, 9)
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

recipes = []

def scrape_page(url):
    resp = requests.get(url, headers=headers)
    resp.encoding = 'utf-8'
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    for block in soup.find_all('div', class_='browse-recipe-content'):
        title_tag = block.find('h2', class_='browse-recipe-name')
        title = title_tag.get_text(strip=True) if title_tag else ''

        desc_tag = block.find('blockquote', class_='browse-recipe-content-description')
        description = desc_tag.get_text(strip=True) if desc_tag else ''

        ingredient_tag = block.find('p', class_='browse-recipe-content-ingredient')
        ingredients = ingredient_tag.get_text(strip=True) if ingredient_tag else ''

        recipes.append({
            '料理名稱': title,
            '簡介': description,
            '使用食材': ingredients
        })

# 爬取所有頁面
for url in urls:
    scrape_page(url)

# 建立 DataFrame
df = pd.DataFrame(recipes)

# 取得用戶輸入數量
try:
    count = int(input(f"請輸入要選取的料理數量 (最多 {len(df)} 筆): "))
    if count < 1 or count > len(df):
        raise ValueError("輸入的數量超出範圍。")
except ValueError as e:
    print("錯誤：請輸入有效數字，且不超過資料總數量。")
    exit(1)

# 隨機選取不重複料理
sample_df = df.sample(n=count, replace=False)
print(sample_df.to_string(index=False))
