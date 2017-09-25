---
layout: page
title: Tablón Cultural
navigation: true
---
{% for post in site.posts %}
{% assign post = site.category.first %}
<section class="post wrapper">
  <h1><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h1>
  <p class="post-meta">{{ post.date | date: "%d/%m/%Y" }}</p>
  {{ post.content | markdownify }}
</section>

{% endfor %}

{% include pagination.html %}
