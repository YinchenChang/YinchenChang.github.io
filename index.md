---
layout: page
title: Andy Chang
lang: en
alt: /zh/
permalink: /
---

I am a fund manager in Taipei. I study AI compute as an economic system: what a gigawatt of capacity can earn, where each dollar of AI capital spending goes, and which parts of the supply chain keep their share.

**Start here**

- [AI Compute Investment Map](map/) — the whole stack on one page, with links to the models behind each layer.
- [Writing](writing/) — essays, published as the research matures.
- [Tokenomics](https://github.com/YinchenChang/Tokenomics) — my open, first-principles model of AI data center economics (interactive app: under maintenance).

**Latest**

{% assign posts = site.posts | where: "lang", "en" %}{% for post in posts limit: 5 %}
- {{ post.date | date: "%Y-%m-%d" }} · [{{ post.title }}]({{ post.url | relative_url }})<span data-new="{{ post.date | date: '%Y-%m-%d' }}"></span>
{% endfor %}
