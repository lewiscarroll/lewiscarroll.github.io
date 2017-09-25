---
layout: page
title: Actividades
navigation: true
---

<div class="posts">
{% for post in site.categories.cultura %}
<section class="post wrapper">
  <h1><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h1>
  <p class="post-meta">{{ post.date | date: "%d/%m/%Y" }}</p>
  {{ post.content | markdownify }}
</section>
{% endfor %}
</div><!--/posts-->
