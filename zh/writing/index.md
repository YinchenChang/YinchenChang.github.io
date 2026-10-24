---
layout: page
title: 文章
permalink: /zh/writing/
lang: zh
alt: /writing/
---

{% assign posts = site.posts | where: "lang", "zh" %}{% for post in posts %}
- {{ post.date | date: "%Y-%m-%d" }} · [{{ post.title }}]({{ post.url | relative_url }})
{% endfor %}
