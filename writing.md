---
layout: page
title: Writing
permalink: /writing/
lang: en
alt: /zh/writing/
---

{% assign posts = site.posts | where: "lang", "en" %}{% for post in posts %}
- {{ post.date | date: "%Y-%m-%d" }} · [{{ post.title }}]({{ post.url | relative_url }})<span data-new="{{ post.date | date: '%Y-%m-%d' }}"></span>
{% endfor %}
