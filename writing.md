---
layout: page
title: Writing
permalink: /writing/
---

{% if site.posts.size == 0 %}
The first essays are being edited. They will appear here.
{% else %}
{% for post in site.posts %}
- {{ post.date | date: "%Y-%m-%d" }} · [{{ post.title }}]({{ post.url | relative_url }})
{% endfor %}
{% endif %}
