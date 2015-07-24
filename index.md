---
layout: home
---

<div class="home">
<div class="logo-bar">

  <h1 class="page-heading">Posts</h1>

    <ul>
      {% for post in site.posts %}
        <li>
          <a href="{{ post.url }}">{{ post.title }}</a>
          <p>{{ post.excerpt }}</p>
        </li>
      {% endfor %}
    </ul>


  <p class="rss-subscribe">subscribe <a href="{{ "/feed.xml" | prepend: site.baseurl }}">via RSS</a></p>

</div>
