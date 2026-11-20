# BlueTrace | 作業系統期末專題網站（淺藍色漸層版）

本網站依據老師的 `Operating Systems — Final Project: Experimental Analysis of Real-World Operating Systems` 規定，選擇 **Topic 2: CPU and Memory Resource Analysis in Real Computing Systems**。網站是 Week 1 可開始使用的 **正式報告框架**，不是已完成分析的期末報告。

## 老師要求對照

| 老師規定 | 網站位置／實作狀態 |
| --- | --- |
| Introduction：研究動機、目標、至少兩個可測研究問題 | `#introduction`：目前已有三題研究問題 |
| Dataset：來源、欄位、資料範圍、清理 | `#dataset`：官方 2017 Schema、清理欄位與待補數據 |
| Methodology：流程、工具、評估指標 | `#methodology`：三種分析設計與預設門檻（待組員確認） |
| Results：至少五張圖表，有標題、單位、說明、分析 | `#results`：準備七張圖表位置；真實 CSV 分析後由 Python 輸出 PNG，初版**尚未完成** |
| Discussion：作業系統概念、限制 | `#discussion`：討論框架，需依實際結果改寫 |
| Conclusion：研究結論 | `#conclusion`：預留位置，未捏造結論 |
| References & reproducibility：來源、程式、依賴、重現方式 | `#references`、`requirements.txt`、`analysis/analyze.py` |
| 每名組員貢獻說明 | `#references` 下方 A–F 表格，最終請更換真實姓名 |
| 專題網站＋程式碼庫網址 | GitHub Pages 可部署；**仍需自行上傳才有公開 URL** |
| 8–10 分鐘小組報告 | 報告由全組共同完成；本網站可用於現場展示 |

**重要：** 老師明確指定 Alibaba Cluster Trace **2017**（並非 2018）。我們暫定 `server_usage.csv`，與老師的 CPU、Memory、Load Average 欄位要求一致。最終資料選用需全組確認。

## 先看網頁

雙擊根目錄下的 `index.html` 即可使用。HTML、CSS、JS 不需要 Node、npm 或資料庫；可在手機／電腦瀏覽器開啟。首頁顯示的線條插圖是**裝飾圖案，不是真實研究數據**。

## W1：F（網站負責人）現在能做的事情

1. 確認網站標題、專題 Topic、研究問題是否與組員一致。
2. 建立 GitHub Repo，把這個資料夾的**內容**（`index.html` 應在最外層）上傳。
3. `Settings → Pages → Build and deployment → Deploy from a branch → main → /(root) → Save`。
4. 和 A 討論資料處理後提供 CSV／圖表的檔案格式，並和 B～E 約定交稿內容（**圖表＋單位＋caption＋統計解釋**）。
5. 先測試頁面在手機和電腦的排版；不要把預留圖表當成已完成的研究結果。

## W2–W3：實際資料如何變成圖表？

### A. 純瀏覽器互動預覽（少量資料）

在網站 `Results` → `Interactive Data Explorer` 選擇 v2017 `server_usage.csv` 的小型樣本：
- 檔案大小最多 6 MB；最多讀取前 30,000 列資料；
- CSV 第一至第四欄應是 `timestamp,machineID,util:CPU,util:memory`；可使用官方 8 欄無標頭格式；
- 可選 CPU／Memory、選擇機器，並看到真實的樣本折線圖；
- CSV 不會上傳到伺服器；只在自己的瀏覽器處理。

**瀏覽器預覽不是正式研究結果**；圖表可能受小樣本範圍與時間取樣影響。

### B. 正式圖表（建議給 A–E 組員使用）

從阿里巴巴官方取得 2017 `server_usage.csv`，安裝 Python 套件：

```bash
pip install -r requirements.txt
python analysis/analyze.py --input /path/to/server_usage.csv
```

執行位置要在本專案根目錄，輸出會寫入 `assets/results/`：

- `fig01_cpu_histogram.png` — CPU 使用率直方圖
- `fig02_cpu_time_series.png` — CPU 時間序列圖
- `fig03_machine_comparison.png` — 機器平均 CPU 比較
- `fig04_memory_histogram.png` — Memory 直方圖
- `fig05_cpu_memory_scatter.png` — CPU–Memory 散佈圖
- `fig06_imbalance_heatmap.png` — 不同機器／時間資源使用率 Heatmap
- `fig07_utilization_categories.png` — Low／Medium／High 類別比例
- `results.js`、`analysis_summary.json` — 分析數據、選樣設定與說明
- `machine_summary.csv`、`category_transitions.csv` — 補充比較表及類別轉換統計

網站載入 `results.js` 後會自動顯示完成的 PNG 與數值摘要。如果原始檔過大，請調高 `--every 10`、`--every 20` 等，系統會記錄抽樣規則。抽樣使用固定亂數種子（預設 42），以每列機率 1/N 獨立選取，避免依照檔案列排序每 N 列抽一筆所造成的週期偏差。若超過 `--max-selected`，程式會報錯，**不會偷偷截斷只取前段時間的資料**。

預設門檻 low <= 30%、medium 30–70%、high > 70%，是我們的*提案*，不是老師或官方規定。可透過 `--low 25 --high 75` 調整，但全組必須一致並解釋理由。

### 數據解釋要補什麼？

圖表產生後仍需 B～E：
- 對每張圖寫**具體**結果，不只「圖中有高低」。
- 描述選用哪部分資料、比較了哪些機器或時間。
- 連結作業系統的 CPU／Memory、資源分配、排程議題。
- 提及 2017 traces 的觀察範圍、抽樣限制與「高使用率不等於效能差」。
- 更新 Discussion、Conclusion、報告上傳日期與每人貢獻。

## GitHub Pages 部署

1. 登入 GitHub，建立新 Repository，例如 `os-blue-trace`。
2. 將 ZIP 解壓縮，**把所有內容**上傳到 Repository 根目錄。
3. 專案 `Settings → Pages` → 選擇 `Deploy from a branch` → `main` / `(root)` → `Save`。
4. GitHub 建立後，網址大致形如 `https://USERNAME.github.io/os-blue-trace/`，需實際開啟檢查。
5. W3/W4 把真實分析輸出 `assets/results/*` 重新上傳，網頁就會顯示圖片。

老師要求最後交：**公開網站 URL、程式碼 Repo URL、至少五張有分析的圖表、8–10 分鐘組報告、個別貢獻說明**。

## 檔案結構

```text
OS_Blue_Gradient_Project/
├── index.html                      # 入口網頁，淺藍漸層 UI
├── assets/
│   ├── app.js                      # 導覽、CSV 預覽、讀取真實分析成果
│   └── results/
│       └── results.js             # 初始空白；分析後自動更新
├── analysis/
│   └── analyze.py                  # 可重現的資料分析與製圖程式
├── requirements.txt               # Python dependencies
├── .nojekyll                       # Pages 靜態資源支援
└── README.md                       # 說明與注意事項
```

## 官方參考資料

- 老師提供的課堂 PDF（由組員自行保管；此專案包不另行公開傳送）
- [Alibaba Cluster Trace](https://github.com/alibaba/clusterdata)
- [Alibaba 2017 trace description](https://github.com/alibaba/clusterdata/blob/master/cluster-trace-v2017/trace_201708.md)
- [Alibaba 2017 schema.csv](https://github.com/alibaba/clusterdata/blob/master/cluster-trace-v2017/schema.csv)
- [GitHub Pages 設定文件](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
