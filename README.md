# GroupProject - team 8 吉伊卡哇氣象報報

## [連結按我](https://wehelp-groupproject.onrender.com/)

## 氣象資訊 User Story

> 氣象局API [Swagger](https://opendata.cwa.gov.tw/dist/opendata-swagger.html#/)

1. 使用者想要概覽全台灣各縣市今日氣溫、降雨機率，作為出遊或問候時的參考
2. 使用者想要特定縣市36小時內天氣預報，包括氣溫、降雨機率、天氣概況與體感舒適度，作為近期出門穿搭與攜帶雨具的參考。[表格參考](https://www.cwa.gov.tw/V8/C/W/County/index.html)
3. 使用者想要知道特定縣市五日內熱傷害警示與當天紫外線強度，作為今天是否適合戶外活動的依據。[呈現方式參考1](https://crowa.cwa.gov.tw/HealthWeather/),[呈現方式參考2](https://www.cwa.gov.tw/V8/C/W/OBS_UVI.html)呈現/要擦防曬
4. 使用者想要每天早上在Discord上收到當日氣象簡述，作為出門前的提醒。

## 開發優先序

```py
1+2 > 5 > 3 > 4 > 6
```

## EPIC, STORY & TASK

1. 顯示全台灣未來36小時天氣
    1. 以表格顯示全台灣天氣狀況、降雨機率圖示
    2. 特定地區未來36小時內的天氣、氣溫區間與降雨情況
        1. front-end: 1 html RWD, 點擊表格/懸浮可以顯示特定地區(call back-end api & render) [參考](https://nomadlist.com/)
        2. back-end
            1. API1: 回應全台灣氣象與降雨機率的JSON
            2. API2: 根據query的縣市回應該地區未來36小時內的天氣、氣溫區間與降雨情況
            3. 確認call api的時間點回傳的資料內容，不需要做資料庫
2. 顯示各縣市當日最大紫外線指數與熱傷害燈號
    1. 以表格與下拉式選單顯示當日最大紫外線指數
    2. 以表格與下拉式選單底色顯示當日熱傷害警示，並以未來五日最大值作圖
        1. front-end: 1 html RWD, 中間各縣市表格，左邊是選擇中縣市的紫外線，右邊是該縣市外來五日的熱指數周報 [參考](https://crowa.cwa.gov.tw/HealthWeather/)
        2. back-end
            1. API: 提供以縣市為參數的當日區域內最大紫外線指數和未來5日的最大熱傷害指數與燈號(以區為主)

## Construct

- app
  - config
    - basemodel.py: APIs respond/request model
  - routers
    - weather.py: API router of task 1 & 2
    - warning.py: API router of task 3 & 4
    - discord.py: API router of task 5
  - view
    - county.js
    - index.js
    - warning.js
  - main.py: Controller
- public
  - css
    - basic.css: CSS for basic compartments
    - index.css: CSS for index.html specific elements
    - county.css: CSS for county.html specific elements
    - warning.css: CSS for warning.html specific elements
  - images: image resources
- static
  - index.html: HTML for task 1
  - county.html: HTML for task 2
  - warning.html: HTML for task 3 & 4
- .gitignore
- README.md

## Environment

1. Server Host: Render
2. Packages:
    1. fastapi
    2. pydantic.basemodel
    3. APScheduler
    4. requests
    5. datetime

## Works

### day1

1. 組長(昊)：分MVC架構，repository
2. 後端(書硯): 定義API規格(了解氣象局API回傳資料)，Model Class(respond/request)
3. 前端(聖鎧/宜群): navbar與基礎背景切版, 提出資料需求, static規劃(表格分三時段顯示，縣市點進去redirect county.html render)

### day2

1. 陳昊: main.py & discord bot
2. 書硯: weather.py router and basemodel.py
3. 聖鎧: county.html 主畫面部分 RWD
4. 宜群: index.html 主畫面部分 RWD & navbar/footer
5. 20:00 daily sprint

### day3

1. 陳昊: warning.py router, discordBot.py  basemodel.py
2. 書硯: weather cache/ api modify and a little basemodel.py
3. 聖鎧: warning.html
4. 宜群: navbar 連結 / UX
5. 22:00 daily sprint

### day4

1. 陳昊: warning cache, discord bot
2. 書硯: render or EC2 佈署
3. 聖鎧: warning.html api/ county,warning RWD
4. 宜群: index 台灣圖 RWD, UX 3 html
5. discussion after Martin sharing
