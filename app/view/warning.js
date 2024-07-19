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
  "連江縣",
];
const AREA = {};
const PURPLE = {};
let COUNTY = "臺北市";
let TOWN = "信義區";
let myChart;
async function getData() {
  const res = await fetch("/api/hotdamage");
  const data = await res.json();
  return data;
}
async function getPurple() {
  const res = await fetch("/api/UV");
  const data = await res.json();
  return data;
}

const DATA = await getData();
const Purple = await getPurple();

DATA.data.forEach((item) => {
  const array = {};
  item.data.forEach((i) => {
    array[i.town] = i.data;
  });
  AREA[item.county] = array;
});
Purple.data.forEach((item) => {
  PURPLE[item.county] = item.UVIndex;
});

function get_purple() {
  const num = document.querySelector(".title__purple--img");
  const tag = document.querySelector(".title__purple--tag");
  if (PURPLE[COUNTY]) {
    num.innerText = PURPLE[COUNTY];
  } else {
    num.innerText = "X";
  }
  if (PURPLE[COUNTY] < 3) {
    tag.innerHTML = "低量級";
  } else if (PURPLE[COUNTY] < 6) {
    tag.innerHTML = "中量級";
  } else if (PURPLE[COUNTY] < 8) {
    tag.innerHTML = "高量級";
  } else if (PURPLE[COUNTY] < 11) {
    tag.innerHTML = "過量級";
  } else if (PURPLE[COUNTY] >= 11) {
    tag.innerHTML = "危險級";
  } else {
    tag.innerHTML = "此行政區沒有觀測站";
  }
}

function init_data() {
  const btn = document.querySelector(".title__btn");
  const btntext = document.createElement("span");
  btntext.innerText = COUNTY;
  btntext.id = "btn__span";
  const tri = document.createElement("div");
  tri.classList.add("title__btn--tri");
  btn.appendChild(btntext);
  btn.appendChild(tri);
  const hot_title = document.querySelector(".hot__title");
  if (TOWN) {
    hot_title.innerText = `${TOWN} 熱指數週報`;
  } else {
    hot_title.innerText = `熱指數週報`;
  }
}

function create_list() {
  const container = document.querySelector(".title__list");
  const tri = document.querySelector(".title__btn--tri");
  const area = document.querySelector(".area__itemContainer");
  TaiwanCities.forEach((item) => {
    const i = document.createElement("div");
    i.classList.add("title__listItem");
    i.innerText = item;
    i.addEventListener("click", (e) => {
      COUNTY = item;
      TOWN = (Object.keys(AREA[COUNTY]))[0];
      const btn = document.querySelector("#btn__span");
      btn.textContent = item;
      container.classList.remove("open");
      tri.classList.remove("no_tri");
      area.innerText = "";
      create_area();
      const hot_title = document.querySelector(".hot__title");
      if (TOWN) {
        hot_title.innerText = `${TOWN} 熱指數週報`;
      } else {
        hot_title.innerText = `熱指數週報`;
      }
      if (myChart) {
        myChart.destroy();
      }
      create_chart();
      get_purple();
    });
    container.appendChild(i);
  });
}

function click_title_btn() {
  const btn = document.querySelector(".title__btn");
  const tri = document.querySelector(".title__btn--tri");
  btn.addEventListener("click", () => {
    const list = document.querySelector(".title__list");
    list.classList.add("open");
    tri.classList.add("no_tri");
  });
}

function create_area() {
  Object.keys(AREA[COUNTY]).map((item) => {
    const container = document.querySelector(".area__itemContainer");
    const i = document.createElement("div");
    i.classList.add("area__item");
    if (AREA[COUNTY][item][0].maxWarning === "高危險") {
      i.classList.add("black");
    } else if (AREA[COUNTY][item][0].maxWarning === "危險") {
      i.classList.add("red");
    } else if (AREA[COUNTY][item][0].maxWarning === "警戒") {
      i.classList.add("orange");
    } else if (AREA[COUNTY][item][0].maxWarning === "注意") {
      i.classList.add("yellow");
    }
    i.innerText = item;
    i.addEventListener("click", () => {
      TOWN = item;
      if (myChart) {
        myChart.destroy();
      }
      create_chart();
      const hot_title = document.querySelector(".hot__title");
      hot_title.innerText = `${TOWN} 熱指數週報`;
    });
    container.appendChild(i);
  });
}

function check_click_title_btn() {
  document.addEventListener("click", (e) => {
    const div = document.querySelector(".title__listContainer");
    const list = document.querySelector(".title__list");
    const tri = document.querySelector(".title__btn--tri");
    if (!div.contains(e.target)) {
      list.classList.remove("open");
      tri.classList.remove("no_tri");
    }
  });
}
function show_purple_tag() {
  const i = document.querySelector(".title__purple--img");
  const tag = document.querySelector(".title__purple--tag");
  i.addEventListener("mouseover", (e) => {
    tag.classList.add("open");
    i.addEventListener("mousemove", (event) => {
      tag.style.top = event.pageY + 10 + "px";
      tag.style.left = event.pageX + 10 + "px";
    });
  });
  i.addEventListener("mouseout", (e) => {
    i.removeEventListener("mousemove", (event) => {
      tag.style.top = event.pageY + 10 + "px";
      tag.style.left = event.pageX + 10 + "px";
    });
    tag.classList.remove("open");
  });
}

function hover_map() {
  const taiwan = document.querySelectorAll("g");
  const tag = document.querySelector(".map__tag");
  const area = document.querySelector(".area__itemContainer");
  taiwan.forEach((e) => {
    let i = e.querySelector("desc");
    let name = i.textContent.substring(0, 3);
    e.addEventListener("mouseover", () => {
      tag.classList.add("open");
      tag.innerText = name;
      e.addEventListener("mousemove", (event) => {
        tag.style.top = event.pageY - 200 + "px";
        tag.style.left = event.pageX + 10 + "px";
      });
    });
    e.addEventListener("mouseout", () => {
      tag.classList.remove("open");
      e.removeEventListener("mousemove", (event) => {
        tag.style.top = event.pageY - 150 + "px";
        tag.style.left = event.pageX + 10 + "px";
      });
    });
    e.addEventListener("click", () => {
      COUNTY = name;
      TOWN = (Object.keys(AREA[COUNTY]))[0];;
      const btn = document.querySelector("#btn__span");
      btn.textContent = name;
      area.innerText = "";
      create_area();
      const hot_title = document.querySelector(".hot__title");
      if (TOWN) {
        hot_title.innerText = `${TOWN} 熱指數週報`;
      } else {
        hot_title.innerText = `熱指數週報`;
      }
      if (myChart) {
        myChart.destroy();
      }
      create_chart();
      get_purple();
    });
  });
}

function create_chart() {
  const chart = document.querySelector("#mychart");
  const today = new Date();
  const day = today.getDate();
  const week = [
    "星期日",
    "星期一",
    "星期二",
    "星期三",
    "星期四",
    "星期五",
    "星期六",
    "星期日",
    "星期一",
    "星期二",
    "星期三",
  ];
  const weekday = today.getDay();
  const labels4today = [
    week[weekday],
    week[weekday + 1],
    week[weekday + 2],
    week[weekday + 3],
  ];
  const labels4tomorrow = [
    week[weekday + 1],
    week[weekday + 2],
    week[weekday + 3],
    week[weekday + 4],
  ];
  const labels5 = [
    week[weekday],
    week[weekday + 1],
    week[weekday + 2],
    week[weekday + 3],
    week[weekday + 4],
  ];
  let dataset = {};
  if (TOWN) {
    const hotArray = [];
    AREA[COUNTY][TOWN].forEach((i) => {
      hotArray.push(i.maxIndex);
    });
    if (hotArray.length === 4) {
      if (day === parseInt(AREA[COUNTY][TOWN][0].date.substring(8, 10))) {
        dataset.labels = labels4today;
      } else {
        dataset.labels = labels4tomorrow;
      }
    } else if (hotArray.length === 5) {
      dataset.labels = labels5;
    }

    dataset.datasets = [
      {
        label: "熱傷害指數",
        data: hotArray,
        borderColor: ["red"],
      },
    ];
  } else {
    dataset.labels = labels4today;
    dataset.datasets = [
      {
        label: "熱傷害指數",
        data: [],
        borderColor: ["red"],
      },
    ];
  }
  myChart = new Chart(chart, {
    type: "line",
    data: dataset,
    options: {
      scales: {
        y: {
          suggestedMin: 25,
          suggestedMax: 45,
        },
      },
      plugins: {
        legend: {
          labels: {
            // This more specific font property overrides the global property
            font: {
              size: 20,
            },
          },
        },
      },
    },
  });
}

function addEventListener() {
  click_title_btn();
  check_click_title_btn();
  show_purple_tag();
  hover_map();
}

function fill_map() {
  const taiwan = document.querySelectorAll("g");
  taiwan.forEach((e) => {
    let i = e.querySelector("desc");
    let path = e.querySelector("path");
    let name = i.textContent.substring(0, 3);
    let city = i.textContent.substring(3, 6);
    if (AREA[name][city][0].maxWarning === "高危險") {
      path.classList.add("fill__black");
    } else if (AREA[name][city][0].maxWarning === "危險") {
      path.classList.add("fill__red");
    } else if (AREA[name][city][0].maxWarning === "警戒") {
      path.classList.add("fill__orange");
    } else if (AREA[name][city][0].maxWarning === "注意") {
      path.classList.add("fill__yellow");
    }
  });
}
const introModal = document.querySelector(".intro-modal");
const questionIcon = document.querySelector(".question-icon");
const overlay = document.querySelector(".overlay");

introModal.style.display = "none";
overlay.style.display = "none";

function clickToShowModal() {
  introModal.style.display = "block";
  overlay.style.display = "block";
}
function closeModal() {
  introModal.style.display = "none";
  overlay.style.display = "none";
}

if (questionIcon) {
  questionIcon.addEventListener("click", (event) => {
    event.stopPropagation();
    clickToShowModal();
  });
}
window.addEventListener("click", (event) => {
  closeModal();
});
introModal.addEventListener("click", (event) => {
  event.stopPropagation();
});
overlay.addEventListener("click", closeModal);

init_data();
create_list();
create_chart();
create_area();
fill_map();
get_purple();
addEventListener();
