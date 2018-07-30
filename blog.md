---
layout: page
title: Blog
permalink: /blog
tags: blog
---


<ul class="list-unstyled">
      {% for post in site.posts %}


<li class="media mb-4">
  <!--<img class="align-self-start mr-3" width=64 src="/images/bio-photo-0.png" alt="">-->
  <div class="media-body bg-light p-3">

    <a class="btn-light" href="{{ post.url | prepend: site.baseurl }}">
      <h4 class="mt-1 mb-1 font-weight-bold"> {{ post.title }}</h4>
      <p class="text-justify">
        {{ post.content | strip_html | truncatewords:30}}
      </p>
    </a>
  </div>
</li>
      {% endfor %}

    <ul>
