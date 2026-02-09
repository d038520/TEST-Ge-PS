import requests
import json
from datetime import datetime

# 1. 設定您要追蹤的關鍵字
KEYWORDS = ["影", "片", "短","製作","宣傳","行銷","AI"]

def fetch_data(keyword):
    # 使用 g0v 的 API 較不會被封鎖
    url = f"https://pcc.g0v.ronny.tw/api/searchbytitle?query={keyword}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('records', [])
    return []

def generate_html(all_tenders):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = ""
    for t in all_tenders:
        # 建立表格列
        rows += f"""
        <tr>
            <td>{t.get('unit_name', 'N/A')}</td>
            <td><a href="https://pcc.g0v.ronny.tw/tender/{t.get('brief', {}).get('type', '')}/{t.get('job_number', '')}" target="_blank">{t.get('brief', {}).get('title', '無標題')}</a></td>
            <td>{t.get('job_number', 'N/A')}</td>
            <td>{t.get('date', 'N/A')}</td>
        </tr>
        """
    
    # 這裡會讀取 HTML 範本並取代變數
    # (為了方便演示，我直接在下面提供完整的 HTML 結構)

if __name__ == "__main__":
    results = []
    for kw in KEYWORDS:
        results.extend(fetch_data(kw))
    # 這裡通常會結合下方的 HTML 進行存檔
