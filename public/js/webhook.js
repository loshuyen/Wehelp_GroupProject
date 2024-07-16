export function discordBot(weather, percip, temp, UV, hotDam){
  let serverUrl = 'https://discord.com/api/webhooks/1162404320399085690/y6pNTIyURc4-ftZIicqF49uzwNTF70bRw_9D1QyVrmxzbwagnXXX-HNW2E6QvzUJVUVS'
  let timestamp = new Date()

  message = {
    username: '第八組吉伊卡哇',
    avatar_url: 'https://static.wikia.nocookie.net/chiikawa/images/c/cc/%E5%90%89%E4%BC%8A_%E5%8A%A8%E7%94%BB.png/revision/latest/scale-to-width/360?cb=20231017103026&path-prefix=zh',
    embeds:[{
      title: '吉伊卡哇的今日氣象',
      type: 'rich',
      description: '要小心壞天氣與奇美拉',
      // url: ''
      timestamp: timestamp.toISOString(),
      color: 1572632,
      footer: {
        text: 'by 聖鎧、書硯、宜群、陳昊'
      },
      thumbnail: {
        url: 'https://img.shoplineapp.com/media/image_clips/663c651251310fa9e599e4c2/original.jpg?1715234066',
        height: 1000,
        width: 1400
      },
      provider: {
        name: 'Wehelp 2nd phase group pj. team 8'
      },
      author: {
        name: '下禮拜三就是睡衣派對!',
        icon_url: 'https://static.wikia.nocookie.net/chiikawa/images/c/cc/%E5%90%89%E4%BC%8A_%E5%8A%A8%E7%94%BB.png/revision/latest/scale-to-width/360?cb=20231017103026&path-prefix=zh'
      },
      fields: [
        {name: '天  氣🌤️', value: weather, inline: true},
        {name: '降  雨🌧️', value: percip, inline: true},
        {name: '氣  溫🌡️', value: temp, inline: true},
        {name: '紫外線🕵️‍♀️', value: UV, inline: true},
        {name: '熱傷害🥵', value: hotDam, inline: true}
      ],
      image: {
        url: 'https://p2.bahamut.com.tw/B/GUILD/f/7/0000015737_background.PNG',
        height: 375,
        width: 1250
      }
    }]
  }

  fetch(`${serverUrl}?wait=true`,{
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(message)
  })

}

