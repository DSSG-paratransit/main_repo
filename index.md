---
layout: home
---

<div class="home">
<div class="logo-bar">

  <h1 class="page-heading">Posts</h1>

  <ul class="post-list">
    {% for post in site.posts %}
      <li class="post-item">
        <h2>
          <a class="post-link" href="{{ post.url | prepend: site.baseurl }}">{{ post.title }}</a>
        </h2>
        <p>{{ post.meta }}</p>
        <p> {{ post.excerpt }} </p>
        <p>
          {% if post.content contains site.excerpt_separator %}
            <a class="post-readmore" href="{{ post.url | prepend: site.baseurl }}">[read more...]</a>
          {% endif %}
        </p>
      </li>
      <br>
    {% endfor %}
  </ul>

  <p class="rss-subscribe">subscribe <a href="{{ "/feed.xml" | prepend: site.baseurl }}">via RSS</a></p>

</div>
