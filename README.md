# GroupProject - team 8

## 氣象資訊 User Story

> 氣象局API [Swagger](https://opendata.cwa.gov.tw/dist/opendata-swagger.html#/)

1. 使用者/欲查詢地區未來36小時內的天氣、氣溫區間與降雨情況/因為想提前應對
2. 使用者/欲查詢全台灣目前的天氣狀況、降雨機率圖示，並以[表格](https://www.cwa.gov.tw/V8/C/W/County/index.html)呈現/想問候當地的朋友時可以參考
3. 使用者/欲查詢地區未來五天中午的熱傷害指數與警戒標示，並以[此方式](https://crowa.cwa.gov.tw/HealthWeather/)呈現/不想被熱死
4. 使用者/欲查詢全台灣當日指外線指數，並以[此方式](https://www.cwa.gov.tw/V8/C/W/OBS_UVI.html)呈現/要擦防曬
5. 使用者/想要在Discord收到Bot傳的每日氣象預報/方便

## 優先序

```py
1+2 > 5 > 3 > 4
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
2. 待定

## Construct

- app
  - config
    - basemodel.py: APIs respond/request model
  - routers
    - weather.py: API router of task 1 & 2
    - warning.py: API router of task 3 & 4
  - view: front-end logic operating DOM
  - main.py: Controller
  - handlers.py: Define actions for exceptions
- public
  - css
    - basic.css: CSS for basic compartments
    - index.css: CSS for index.html specific elements
    - county.css: CSS for county.html specific elements
  - images: image resources
- static
  - index.html: HTML for task 1 & 2
  - county.html: HTML for task 3 & 4
- .env: key storage
- .gitignore
- README.md

## Works

### day1

1. 組長(昊)：分MVC架構，repository
2. 後端(書硯): 定義API規格(了解氣象局API回傳資料)，Model Class(respond/request)
3. 前端(聖鎧/宜群): navbar與基礎背景切版, 提出資料需求, static規劃(表格分三時段顯示，縣市點進去redirect county.html render)
