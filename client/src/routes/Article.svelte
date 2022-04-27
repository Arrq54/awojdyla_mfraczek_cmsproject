<script>
  import { Router, Link } from "svelte-navigator";
  export let params = {};
  let fetchArticle = getArticle(params.id);
  async function getArticle(id) {
    const body = JSON.stringify({ body: id });
    const headers = { "Content-Type": "application/json" };
    let response = await fetch("/getArticleById", {
      method: "post",
      body,
      headers,
    }).then((response) => response.json());
    return response[0];
  }
</script>

{#await fetchArticle then article}
  <h1>{article.title}</h1>
  <h5>{article.text_content}</h5>
  <div class="article-content">{article.content}</div>
  <h1>{article.idnews}</h1>

  <!--
    article.idnews - id z bazy danych
    article.text_content - mniejszy tekst wyswietlany na stronie glownej pod blokiem
    article.title - tytul
    article.content - długi tekst z artykułu, white-space: pre-wrap, robi akapity pod \n, bo tak jest w bazie danych
    -->
{/await}

<style>
  .article-content {
    white-space: pre-wrap;
  }
</style>
