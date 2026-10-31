---
layout: page
title: Andy Chang
lang: zh
alt: /
permalink: /zh/
---

我是台北的基金經理人，把 AI 算力當成一個經濟系統來研究：1 GW 的算力能賺多少、AI 資本支出的每一塊錢流到哪裡、供應鏈的哪些環節守得住份額。

**從這裡開始**

- [AI 算力投資地圖](map/)：整個產業鏈放在一頁，每一層都連到背後的模型。
- [文章](writing/)：研究成熟一篇，發表一篇。
- [Tokenomics](https://github.com/YinchenChang/Tokenomics)：我以第一原理建構的 AI 資料中心經濟模型，公開原始碼（互動應用：維修中）。

**最新文章**

{% assign posts = site.posts | where: "lang", "zh" %}{% for post in posts limit: 5 %}
- {{ post.date | date: "%Y-%m-%d" }} · [{{ post.title }}]({{ post.url | relative_url }})<span data-new="{{ post.date | date: '%Y-%m-%d' }}"></span>
{% endfor %}
