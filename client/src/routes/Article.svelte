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
    console.log(response);
    return response[0];
  }
  let currentGalleryPhoto = 2;
  function setGalleryPhoto(i) {
    currentGalleryPhoto = i;
    document.querySelector("#overlay").style.display = "block";
    document.querySelector("#extended-gallery").style.display = "block";
  }
  function changePhoto(x, article) {
    let pictures = JSON.parse(article.pictures);
    if (currentGalleryPhoto == pictures.length - 1 && x == 1)
      currentGalleryPhoto = 0;
    else if (currentGalleryPhoto == 0 && x == -1)
      currentGalleryPhoto = pictures.length - 1;
    currentGalleryPhoto += x;
  }
  function hideGallery() {
    document.querySelector("#overlay").style.display = "none";
    document.querySelector("#extended-gallery").style.display = "none";
  }
</script>

<svelte:head>
  <link rel="stylesheet" href="../../style/article.css" />
</svelte:head>
{#await fetchArticle then article}
  <h1>{article.title}</h1>
  <h5>{article.text_content}</h5>
  <div class="article-content">{article.content}</div>
  <h1>{article.idnews}</h1>

  <div class="gallery">
    {#each JSON.parse(article.pictures) as picture, i}
      <div class="gallery-item">
        <img
          src={picture}
          alt=""
          class="gallery-picture"
          on:click={() => setGalleryPhoto(i)}
        />
      </div>
    {/each}
  </div>
  <div class="overlay" id="overlay" style="display: none;" />
  <div id="extended-gallery" class="extended-gallery" style="display: none;">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 384 512"
      class="x-sign"
      on:click={() => hideGallery()}
      ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
        d="M376.6 427.5c11.31 13.58 9.484 33.75-4.094 45.06c-5.984 4.984-13.25 7.422-20.47 7.422c-9.172 0-18.27-3.922-24.59-11.52L192 305.1l-135.4 162.5c-6.328 7.594-15.42 11.52-24.59 11.52c-7.219 0-14.48-2.438-20.47-7.422c-13.58-11.31-15.41-31.48-4.094-45.06l142.9-171.5L7.422 84.5C-3.891 70.92-2.063 50.75 11.52 39.44c13.56-11.34 33.73-9.516 45.06 4.094L192 206l135.4-162.5c11.3-13.58 31.48-15.42 45.06-4.094c13.58 11.31 15.41 31.48 4.094 45.06l-142.9 171.5L376.6 427.5z"
      /></svg
    >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 320 512"
      class="arrow left-arrow"
      on:click={() => changePhoto(-1, article)}
      ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
        d="M224 480c-8.188 0-16.38-3.125-22.62-9.375l-192-192c-12.5-12.5-12.5-32.75 0-45.25l192-192c12.5-12.5 32.75-12.5 45.25 0s12.5 32.75 0 45.25L77.25 256l169.4 169.4c12.5 12.5 12.5 32.75 0 45.25C240.4 476.9 232.2 480 224 480z"
      /></svg
    >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 320 512"
      class="arrow right-arrow"
      on:click={() => changePhoto(1, article)}
      ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
        d="M96 480c-8.188 0-16.38-3.125-22.62-9.375c-12.5-12.5-12.5-32.75 0-45.25L242.8 256L73.38 86.63c-12.5-12.5-12.5-32.75 0-45.25s32.75-12.5 45.25 0l192 192c12.5 12.5 12.5 32.75 0 45.25l-192 192C112.4 476.9 104.2 480 96 480z"
      /></svg
    >
    <img src={JSON.parse(article.pictures)[currentGalleryPhoto]} alt="" />
  </div>

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
