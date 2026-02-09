import requests
import json
from datetime import datetime

# 1. 設定您要追蹤的關鍵字
KEYWORDS = ["影片", "短片", "製作", "宣傳", "行銷", "AI"]

def fetch_data(keyword):
    print(f"正在抓取關鍵字: {keyword}...")
    url = f"https://pcc.g0v.ronny.tw/api/searchbytitle?query={keyword}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json().get('records', [])
    except Exception as e:
        print(f"抓取 {keyword} 時發生錯誤: {e}")
    return []

def generate_full_html(all_tenders):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 建立表格內容
    table_rows = ""
    for t in all_tenders:
        brief = t.get('brief', {})
        unit = t.get('unit_name', '未知機關')
        title = brief.get('title', '無標題')
        job_num = t.get('job_number', 'N/A')
        date = t.get('date', 'N/A')
        # 取得 g0v 連結
        link = f"https://pcc.g0v.ronny.tw/tender/{brief.get('type', '')}/{job_num}"
        
        table_rows += f"""
        <tr>
            <td class="ps-4">{unit}</td>
            <td><a href="{link}" target="_blank" class="text-decoration-none fw-bold text-primary">{title}</a></td>
            <td><span class="badge bg-light text-dark">{job_num}</span></td>
            <td>{date}</td>
            <td class="pe-4"><span class="badge rounded-pill bg-success">追蹤中</span></td>
        </tr>
        """

    # 完整 HTML 模板
    full_html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>影片行銷標案自動追蹤</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root {{ --pcc-blue: #0d6efd; }}
        body {{ background-color: #f4f7f6; color: #333; font-family: "Microsoft JhengHei", sans-serif; }}
        .header-section {{ background: linear-gradient(135deg, #0d6efd 0%, #003d99 100%); color: white; padding: 40px 0; margin-bottom: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        .card {{ border: none; border-radius: 12px; }}
        .badge-kw {{ background: rgba(255,255,255,0.2); border: 1px solid white; margin-right: 5px; }}
    </style>
</head>
<body>
<div class="header-section">
    <div class="container">
        <h1 class="display-5 fw-bold">🎬 影片行銷標案監測</h1>
        <p class="lead">
            目前追蹤關鍵字：
            {" ".join([f'<span class="badge badge-kw">{kw}</span>' for kw in KEYWORDS])}
        </p>
        <hr>
        <p class="mb-0">最後自動更新時間：<strong>{now}</strong></p>
    </div>
</div>
<div class="container">
    <div class="card shadow-sm">
        <div class="card-body p-0">
            <div class="table-responsive">
                <table class="table table-hover mb-0 align-middle">
                    <thead class="table-dark">
                        <tr>
                            <th class="ps-4">招標機關</th>
                            <th>標案名稱 (點擊開啟)</th>
                            <th>案號</th>
                            <th>公告日期</th>
                            <th class="pe-4">狀態</th>
                        </tr>
                    </thead>
                    <tbody>
                        {table_rows if table_rows else '<tr><td colspan="5" class="text-center p-5">今日尚無符合關鍵字的標案</td></tr>'}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <div class="mt-4 text-center text-muted small pb-5">
        <p>本頁面由 Python 腳本抓取 g0v API 資料後自動產生</p>
    </div>
</div>
</body>
</html>"""
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(full_html)
    print("成功產生 index.html！")

if __name__ == "__main__":
    unique_tenders = {{}}
    for kw in KEYWORDS:
        records = fetch_data(kw)
        for r in records:
            # 使用案號作為唯一 Key，避免重複
            unique_tenders[r.get('job_number')] = r
    
    # 轉為清單並排序（依日期從新到舊）
    final_list = sorted(unique_tenders.values(), key=lambda x: x.get('date', ''), reverse=True)
    generate_full_html(final_list)
