<script>
  import { Router, Link } from "svelte-navigator";
  export let params = {};
  let charnumber = 150;
  let logged = getLoginStatus();
  let zahalowmordewalo = () => {
    charnumber =
      150 - document.getElementById("new_comment_content").value.length;
    if (charnumber <= 0) {
      document.getElementsByClassName("characternumber")[0].style.color = "red";
      document.getElementById("new_comment_content").value = document
        .getElementById("new_comment_content")
        .value.slice(0, 150);
    } else {
      document.getElementsByClassName("characternumber")[0].style.color =
        "rgb(67, 67, 67)";
    }
    charnumber =
      150 - document.getElementById("new_comment_content").value.length;
  };
  async function getLoginStatus() {
    if (localStorage.getItem("user") != null) {
      const body = JSON.stringify({ username: localStorage.getItem("user") });
      const headers = { "Content-Type": "application/json" };
      let temp = fetch("/checkLoginStatus", {
        method: "post",
        body,
        headers,
      }).then((response) => response.json());
      const res = await temp;
      return res;
    } else {
      return { permission: -1 };
    }
  }
  let article_found = false;
  let fetchArticle = getArticle(params.id);
  async function getArticle(id) {
    try {
      const body = JSON.stringify({ body: id });
      const headers = { "Content-Type": "application/json" };
      let response = await fetch("/getArticleById", {
        method: "post",
        body,
        headers,
      }).then((response) => response.json());
      if (response.length > 0) {
        article_found = true;
      }
      console.log(response);
      return response[0];
    } catch {
      article_found = false;
    }
  }
  let fetchComments = getComments(params.id);
  async function getComments(articleid) {
    try {
      const body = JSON.stringify({ articleid: articleid });
      const headers = { "Content-Type": "application/json" };
      let response = await fetch("/getComments", {
        method: "post",
        body,
        headers,
      }).then((response) => response.json());
      console.log(response);
      return response.reverse();
    } catch {
      article_found = false;
    }
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
    else currentGalleryPhoto += x;
  }
  function hideGallery() {
    document.querySelector("#overlay").style.display = "none";
    document.querySelector("#extended-gallery").style.display = "none";
  }
  let ECD = false;
  let changeColor = () => {
    if (ECD) {
      document.getElementById("new_comment_content").value = "";
      document.getElementById("new_comment_content").style.color = "black";
      document.getElementById("sendbt").disabled = false;
      ECD = false;
    }
  };
  let sendComment = () => {
    let sender = localStorage.getItem("user");
    let content = document.getElementById("new_comment_content").value;

    let datetime = new Date();
    let today =
      String(datetime.getDate()).padStart(2, "0") +
      "." +
      String(datetime.getMonth() + 1).padStart(2, "0") +
      "." +
      datetime.getFullYear();
    let hour =
      String(datetime.getHours()).padStart(2, "0") +
      ":" +
      String(datetime.getMinutes()).padStart(2, "0");

    if (content == "") {
      document.getElementById("new_comment_content").style.color = "red";
      document.getElementById("new_comment_content").value =
        "This must not be empty!";
      document.getElementById("sendbt").disabled = true;
      ECD = true;
    } else {
      let body = JSON.stringify({
        user: sender,
        content: content,
        date: today,
        hour: hour,
        articleid: params.id,
      });
      let headers = { "Content-Type": "application/json" };
      fetch("/addComment", { method: "post", body, headers });
      window.location.reload();
    }
  };
</script>

<svelte:head>
  <link rel="stylesheet" href="../../style/article.css" />
</svelte:head>
{#await fetchArticle then article}
  {#if article_found}
    <div class="article_content">
      <h1>{article.title}</h1>
      <h5>{article.text_content}</h5>
      {#if article.pictures != null}
        {#if JSON.parse(article.pictures).length > 0}
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
          <div
            class="overlay"
            id="overlay"
            style="display: none;"
            on:click={hideGallery}
          />
          <div
            id="extended-gallery"
            class="extended-gallery"
            style="display: none;"
          >
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
            <img
              class="extended-gallery-picture"
              src={JSON.parse(article.pictures)[currentGalleryPhoto]}
              alt=""
            />
          </div>
        {/if}
      {/if}

      <div class="article-content">{article.content}</div>
    </div>
  {:else}
    <h1 style="text-align: ;center">This article does not exists</h1>
  {/if}
{/await}
{#if article_found}
  <div class="comments">
    <div class="new_comment">
      {#await logged then status}
        {#if status.permission >= 0}
          <div class="user">
            <img
              src="./images/avatar.png"
              alt="avatar"
              width="65px"
              height="65px"
            />
            <h4>You</h4>
          </div>
          <textarea
            id="new_comment_content"
            on:click={changeColor}
            on:input={zahalowmordewalo}
            rows="3"
          />
          <div class="agagagaga">
            <button on:click={sendComment} id="sendbt">Send</button>
            <div class="characternumber">{charnumber}/150</div>
          </div>
        {:else}
          <div class="user">
            <img
              src="./images/avatar.png"
              alt="avatar"
              width="65px"
              height="65px"
            />
            <h4>Guest</h4>
          </div>
          <textarea
            disabled
            id="new_comment_content"
            on:click={changeColor}
            rows="3"
            style="font-size:150%; text-align:center; padding-top:20px;"
            >You need to log in!</textarea
          >
          <button
            on:click={sendComment}
            disabled
            style="background-color:#6b988f;">Send</button
          >
        {/if}
      {/await}
    </div>
    <div class="load_comments">
      {#await fetchComments then comments}
        {#each comments as comment}
          <div class="comment">
            <div class="user">
              <img
                src="./images/avatar.png"
                alt="avatar"
                width="57px"
                height="57px"
              />
              <h4>{comment[0]}</h4>
            </div>
            <div class="content">{comment[1]}</div>
            <h5 class="time">{comment[2]}</h5>
          </div>
        {/each}
      {/await}
    </div>
  </div>
{/if}

<style>
</style>
