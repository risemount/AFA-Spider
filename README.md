# afa-spider (農情蜘蛛-阿發)
<img src="cute_spider.png" width="300" height="300">

*AFA-Spider* 是用來協助研究人員收集農業部的[農情報告資源網](https://agr.afa.gov.tw/)之農情調查資料，為臺灣農業發展相關研究提供便利的資料收集工具。

## 農情蜘蛛-阿發 版本 0.2 測試版 (2024/07/30 更新)

### 毋須安裝 !!

下載 [AFA_Spider.exe](https://raw.githubusercontent.com/risemount/AFA-Spider/main/AFA_Spider.exe) 應用程式，即可使用。

### 2024/07/30 更新: 新增輸出資料之設定

可選擇各別資料輸出(每一個選項組合分別輸出一個檔案)，或是整理為單一的 batch_data.csv 檔案。然而，此功能在一般作物查詢時需要注意，不同作物類別的變數名稱可能會不一樣，例如: 大部分的穀類作物會以「收穫面積」代表可收穫作物之面積大小，但是，果樹類作物則會以「結實面積」表示。

## 使用說明 (Directions)
### (1) 開啟應用程式時，程式會自動從下載農情報告資源網的網頁選項，並在同一個資料夾內，存取 `web_options.db` 檔案。**勿刪除此檔案，確保程式運行**

<img src="/guidance/guide01.png" width="400" height="280">

### (2) 接下來，請在 **相同資料夾** 底下，新增 `response` 資料夾，作為儲存檔案的路徑 (程式內的 設定 >> 儲存至 亦可調整儲存路徑)。

<img src="/guidance/guide02.png" width="400" height="280">

### (3) 開啟應用程式之後，會顯示使用者介面，可選擇想要下載的資料

<img src="/guidance/guide03.png" width="600" height="590">

### (4) 利用選單的 「設定」 >> 「查詢模式」，可以選擇不同的查詢模式。分別為「稻作查詢」及「一般作物查詢」與「鄉鎮資料」及「縣市資料」

<img src="/guidance/guide04.png" width="600" height="590">

### (5) 選擇要下載的資料之後，在下方的白框會顯示已選擇的選項

<img src="/guidance/guide05.png" width="600" height="590">

### (6) 如果想要清空、並重新選擇選項，可以點選上方的更新

<img src="/guidance/guide06.png" width="600" height="590">

### (7) 開始下載前，可以自行設定儲存路徑，位置在「設定」 >> 「儲存至」

<img src="/guidance/guide07.png" width="600" height="590">

### (8) 如果網頁有更新選項 (例如最新年份的資料已釋出，年份的選項即需要更新)，可以點選「更新選項資料庫」

<img src="/guidance/guide08.png" width="600" height="590">

### (9) 點選下方的「開始」，即可開始下載資料至儲存路徑資料夾。完成時，進度條會顯示綠色全滿，程式即執行完畢。

<img src="/guidance/guide09.png" width="600" height="590">

### (10) 2024/07/30 更新: 新增「設定」>>「輸出資料」，可選擇各別資料或是將所有選擇的目標整理為單一資料。

<img src="/guidance/guide10.png" width="600" height="590">
