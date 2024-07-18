const TaiwanCities = [
    "臺北市",
    "新北市",
    "桃園市",
    "臺中市",
    "臺南市",
    "高雄市",
    "基隆市",
    "新竹市",
    "嘉義市",
    "新竹縣",
    "苗栗縣",
    "彰化縣",
    "南投縣",
    "雲林縣",
    "嘉義縣",
    "屏東縣",
    "宜蘭縣",
    "花蓮縣",
    "臺東縣",
    "澎湖縣",
    "金門縣",
    "連江縣"
];
// const url = new URL(window.location.href)
// const County = decodeURI(url.pathname.split("/")[1])
const urlObj = new URL(window.location.href)
const params = new URLSearchParams(urlObj.search)
const queryParams = {}
params.forEach((value, key) => {
    queryParams[key] = value;
  })
console.log(queryParams)
const County = queryParams.name


async function get_data(url){
    const res = await fetch(url)
    const data = await res.json()
    return data
}
let Data = await get_data("/api/weather/"+County)

function click_hotdamage(){
    const btn = document.querySelector("#nav-warning")
    btn.addEventListener("click",()=>{
        window.location.href = "/warning"
    })
}

function create_list(n){
    const container = document.querySelector("#container")
    const ul = document.createElement("ul")
    ul.classList.add(`list${n}`)
    container.appendChild(ul)
    TaiwanCities.map((item,index)=>{
        const i = document.createElement("li")
        i.innerText = item
        i.classList.add("list__item")
        if(item === County){
            i.classList.add("list__item--high")
        }
        if(index%4===0 || index%4===1){
            i.classList.add("list__item--gray")
        }
        i.addEventListener("click",(e)=>{
            const county = e.currentTarget.textContent
            const listChild1 = document.querySelectorAll(".list1 *")
            listChild1.forEach(child => {child.classList.remove("list__item--high")})
            const listChild2 = document.querySelectorAll(".list2 *")
            listChild2.forEach(child => {child.classList.remove("list__item--high")})
            e.currentTarget.classList.add("list__item--high")
            update_card(county)
        })
        ul.appendChild(i)
    })

}

async function create_background(){
    const data = Data
    const img = document.querySelector(".background")
    if(data.Wx[0].value.includes("雨")){
        img.src = "/images/water-8622588_1280.png"
    }
    else{
        img.src = "/images/sky-7336915_1280.jpg"
    }
}
function create_card_container(){
    const container = document.querySelector("#container")
    const title = document.createElement("div")
    const box = document.createElement("div")
    title.innerText = County+" 36小時天氣預報"
    title.classList.add("title")
    box.id = "card_container";
    container.appendChild(box)
    box.appendChild(title)
}

async function create_card(n){
    const data = Data
    const tag = document.createElement("div")
    tag.classList.add("card__tag")
    tag.innerText = Data.Wx[n].value


    
    const container = document.querySelector("#card_container")
    const card = document.createElement("div")
    card.classList.add("card")
    const img = document.createElement("div")
    const text_container = document.createElement("div")
    text_container.classList.add("card__textContainer")
    const content_container = document.createElement("div")
    content_container.classList.add("card__contentContainer")
    const time = document.createElement("div")
    time.classList.add("card__time")
    if(data.Wx[n].endTime[12]==="8"){
        img.classList.add("card__sun--img")
        card.classList.add("card__sun")
        if(n===0){
            time.innerText = "今日白天"
        }
        else{
            time.innerText = "明日白天"
        }
    }
    if(data.Wx[n].endTime[12]==="6"){
        img.classList.add("card__moon--img")
        card.classList.add("card__moon")
        text_container.classList.add("card__textContainer--moon")
        if(n===2){
            time.innerText = "明日夜晚"
        }
        else{
            time.innerText = "今日夜晚"
        }
    }
    const tem = document.createElement("div")
    tem.classList.add("card__item")
    tem.innerText = data.MinT[n].value+" - "+data.MaxT[n].value+"°C"
    const rain = document.createElement("div")
    rain.classList.add("card__item")
    rain.innerText ="降雨機率："+ data.PoP[n].value+"%"
    const des = document.createElement("div")
    des.classList.add("card__item")
    des.innerText = data.CI[n].value
    container.appendChild(card)
    card.appendChild(img)
    card.appendChild(text_container)
    document.body.appendChild(tag)
    text_container.appendChild(time)
    text_container.appendChild(content_container)
    content_container.appendChild(tem)
    content_container.appendChild(rain)
    content_container.appendChild(des)

    if(Data.Wx[n].value.includes("雨")){
        for(let i=0;i<24;i+=3){
            setTimeout(()=>{
                const rainy = document.createElement("div")
                rainy.classList.add("rain__fall")
                rainy.style.left = `${i}%`
                card.appendChild(rainy)
            },500*i/5)
            
        }
    }
    if(Data.Wx[n].value.includes("雲")||Data.Wx[n].value.includes("陰")){
        const cloud = document.createElement("div")
        cloud.classList.add("cloud")
        card.appendChild(cloud)
    }

    card.addEventListener("mouseover",(e)=>{
        card.addEventListener("mousemove",(event)=>{
            tag.style.top = event.pageY+10 +"px"
            tag.style.left = event.pageX+10+"px"
        })
        tag.classList.add("open")
    })
    card.addEventListener("mouseout",(e)=>{
        card.removeEventListener("mousemove",(event)=>{
            tag.style.top = event.pageY+10 +"px"
            tag.style.left = event.pageX+10+"px"
        })
        tag.classList.remove("open")
    })
}

async function update_card(county) {
    const data = await get_data("/api/weather/"+county)
    const img = document.querySelector(".background")
    if(data.Wx[0].value.includes("雨")){
        img.src = "/images/water-8622588_1280.png"
    }
    else{
        img.src = "/images/sky-7336915_1280.jpg"
    }
    const container = document.querySelector("#card_container")
    container.innerHTML = ""
    const title = document.createElement("div")
    title.innerText = county+" 36小時天氣預報"
    title.classList.add("title")
    container.appendChild(title)
    for(let n = 0; n < 3; n++) {
        const tag = document.createElement("div")
        tag.classList.add("card__tag")
        tag.innerText = data.Wx[n].value
    
        const card = document.createElement("div")
        card.classList.add("card")
        const img = document.createElement("div")
        const text_container = document.createElement("div")
        text_container.classList.add("card__textContainer")
        const content_container = document.createElement("div")
        content_container.classList.add("card__contentContainer")
        const time = document.createElement("div")
        time.classList.add("card__time")
        if(data.Wx[n].endTime[12]==="8"){
            img.classList.add("card__sun--img")
            card.classList.add("card__sun")
            if(n===0){
                time.innerText = "今日白天"
            }
            else{
                time.innerText = "明日白天"
            }
        }
        if(data.Wx[n].endTime[12]==="6"){
            img.classList.add("card__moon--img")
            card.classList.add("card__moon")
            text_container.classList.add("card__textContainer--moon")
            if(n===2){
                time.innerText = "明日夜晚"
            }
            else{
                time.innerText = "今日夜晚"
            }
        }
        const tem = document.createElement("div")
        tem.classList.add("card__item")
        tem.innerText = data.MinT[n].value+" - "+data.MaxT[n].value+"°C"
        const rain = document.createElement("div")
        rain.classList.add("card__item")
        rain.innerText ="降雨機率："+ data.PoP[n].value+"%"
        const des = document.createElement("div")
        des.classList.add("card__item")
        des.innerText = data.CI[n].value
        container.appendChild(card)
        card.appendChild(img)
        card.appendChild(text_container)
        document.body.appendChild(tag)
        text_container.appendChild(time)
        text_container.appendChild(content_container)
        content_container.appendChild(tem)
        content_container.appendChild(rain)
        content_container.appendChild(des)
    
        if(data.Wx[n].value.includes("雨")){
            for(let i=0;i<24;i+=3){
                setTimeout(()=>{
                    const rainy = document.createElement("div")
                    rainy.classList.add("rain__fall")
                    rainy.style.left = `${i}%`
                    card.appendChild(rainy)
                },500*i/5)
                
            }
        }
        if(data.Wx[n].value.includes("雲")||data.Wx[n].value.includes("陰")){
            const cloud = document.createElement("div")
            cloud.classList.add("cloud")
            card.appendChild(cloud)
        }
    
        card.addEventListener("mouseover",(e)=>{
            card.addEventListener("mousemove",(event)=>{
                tag.style.top = event.pageY+10 +"px"
                tag.style.left = event.pageX+10+"px"
            })
            tag.classList.add("open")
        })
        card.addEventListener("mouseout",(e)=>{
            card.removeEventListener("mousemove",(event)=>{
                tag.style.top = event.pageY+10 +"px"
                tag.style.left = event.pageX+10+"px"
            })
            tag.classList.remove("open")
        })

    }
}
create_background()
create_list(1)
create_card_container()
create_card(0)
create_card(1)
create_card(2)
create_list(2)
click_hotdamage()