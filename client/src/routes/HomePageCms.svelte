<script>
  import { Router, Link } from "svelte-navigator";

  async function getContentFromDatabase() {
    let temp = fetch("/getContentFromDatabase").then((response) =>
      response.json()
    );
    const res = await temp;
    console.log(res);
    return res;
  }
  let promiseData = getContentFromDatabase();

  let actualSliderSide = 0;

  function changeSliderSide(x, dataFromDatabase) {
    if (actualSliderSide == 0 && x == -1) {
      actualSliderSide = 2;
    } else if (
      actualSliderSide == dataFromDatabase.slider.length - 1 &&
      x == 1
    ) {
      actualSliderSide = 0;
    } else {
      actualSliderSide += x;
    }
  }
</script>

{#await promiseData then dataFromDatabase}
  <div class="main">
    <!--NAVBAR MENU-->
    <div class="navbar flex justify-space-between">
      <div class="flex">
        <div class="navbar-item">Icon</div>
        <Router>
          {#each dataFromDatabase.navbarItems as item}
            <div class="navbar-item"><Link to={item[0]}>{item[0]}</Link></div>
          {/each}
        </Router>
      </div>

      <div class="register-login-buttons flex">
        <div class="navbar-item btn  btn-login">
          <a href="/#/login" class="btn-a">Login</a>
        </div>
        <div class="navbar-item btn btn-register">
          <a href="/#/register" class="btn-a ">Register</a>
        </div>
      </div>
    </div>
    <!--SLIDER to do-->
    <div
      class="slider"
      style="background-image: url({dataFromDatabase.slider[actualSliderSide]
        .src});"
    >
      <div
        class="arrow arrow-left"
        on:click={() => changeSliderSide(-1, dataFromDatabase)}
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512"
          ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
            d="M224 480c-8.188 0-16.38-3.125-22.62-9.375l-192-192c-12.5-12.5-12.5-32.75 0-45.25l192-192c12.5-12.5 32.75-12.5 45.25 0s12.5 32.75 0 45.25L77.25 256l169.4 169.4c12.5 12.5 12.5 32.75 0 45.25C240.4 476.9 232.2 480 224 480z"
          /></svg
        >
      </div>
      <div
        class="arrow arrow-right"
        on:click={() => changeSliderSide(1, dataFromDatabase)}
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512"
          ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
            d="M96 480c-8.188 0-16.38-3.125-22.62-9.375c-12.5-12.5-12.5-32.75 0-45.25L242.8 256L73.38 86.63c-12.5-12.5-12.5-32.75 0-45.25s32.75-12.5 45.25 0l192 192c12.5 12.5 12.5 32.75 0 45.25l-192 192C112.4 476.9 104.2 480 96 480z"
          /></svg
        >
      </div>
      <div class="slider-content">
        <h4>{dataFromDatabase.slider[actualSliderSide].label}</h4>
        <p>{dataFromDatabase.slider[actualSliderSide].texts}</p>
      </div>
    </div>

    <div class="flex justify-content-center news flex-wrap">
      {#each dataFromDatabase.news as news}
        <div class="newsBlock">
          <div class="news-header">{news.header}</div>
          <div class="news-content">
            <p class="title">{news.title}</p>
            {news.text_content}
            <br />
            <br />
            <div class="btn btn-div-news">
              <a href={news.src} class="btn-news">{news.button_text}</a>
            </div>
          </div>
        </div>
      {/each}
    </div>
    <hr />
    <div class="first-featurette-news flex justify-space-between">
      <div class="ffn-content">
        <div>
          <h3>{dataFromDatabase.firstFeaturetteNews[0].title}</h3>
          <p>{dataFromDatabase.firstFeaturetteNews[0].textContent}</p>
        </div>
      </div>
      <div
        class="ffn-image"
        style="background-image: url({dataFromDatabase.firstFeaturetteNews[0]
          .src});"
      />
    </div>
    <hr />
    <div class="footer">
      <div class="upper-footer flex justify-content-center">
        <Router>
          {#each dataFromDatabase.footer.links as item}
            <div class="footer-item"><Link to={item[0]}>{item[0]}</Link></div>
          {/each}
        </Router>
      </div>
      <hr />
      <div class="lower-footer">
        <h4 class="copyright">{dataFromDatabase.footer.company}</h4>
      </div>
    </div>
  </div>
{/await}

<style>
  .main {
    background-color: white;
    width: 100vw;
    height: 100vh;
  }
  .justify-content-center {
    justify-content: center;
  }
  .justify-space-between {
    justify-content: space-between;
  }
  .flex-wrap {
    flex-wrap: wrap;
  }
  .flex-column {
    flex-direction: column;
  }
  .navbar-item {
    margin: 5px 20px;
    padding: 4px;
  }
  .navbar {
    padding: 0 20%;
    margin-bottom: 10px;
  }
  .flex {
    display: flex;
  }
  .slider {
    width: 100%;
    height: 500px;
    position: relative;
  }
  .arrow {
    width: 20px;
    height: 100px;
    position: absolute;
    top: 50%;
    cursor: pointer;
    transition: 0.5s all ease;
  }
  .arrow:hover {
    transition: 0.5s all ease;
    transform: translateY(-10px);
  }
  .arrow-left {
    left: 5%;
  }
  .arrow-right {
    right: 5%;
  }
  .slider-content {
    position: absolute;
    bottom: 20px;
    width: 500px;
    left: calc(50% - 250px);
    text-align: center;
  }
  .btn {
    border-radius: 5px;
    padding: 4px;
    border: 1px solid black;
  }
  .btn-a {
    padding: 20px;
  }
  .btn-login {
    border: 1px solid #1f8a59;
    background-color: white;
    transition: 0.3s all ease-in-out;
  }
  .btn-register {
    border: 1px solid #1b76fd;
    background-color: white;
    transition: 0.3s all ease-in-out;
  }
  .btn-login > a {
    color: #1f8a59;
    text-decoration: none;
  }
  .btn-login:hover {
    color: white;
    background-color: #1f8a59;
    transition: 0.3s all ease-in-out;
  }
  .btn-login:hover > a {
    color: white;
    transition: 0.3s all ease-in-out;
  }
  .btn-register > a {
    color: #1b76fd;
    text-decoration: none;
  }
  .btn-register:hover {
    color: white;
    background-color: #1b76fd;
    transition: 0.3s all ease-in-out;
  }
  .btn-register:hover > a {
    color: white;
    transition: 0.3s all ease-in-out;
  }

  .news {
    margin-top: 35px;
  }
  .newsBlock {
    width: 400px;
    min-height: 200px;
    border: 1px solid rgb(172, 172, 172);
    margin: 15px;
    border-radius: 3px;
  }
  .news-header {
    background-color: rgb(236, 236, 236);
    border-bottom: 1px solid rgb(172, 172, 172);
    padding: 7px;
  }
  .news-content {
    padding: 10px;
  }
  .title {
    font-size: large;
    font-weight: bold;
  }
  .btn-news {
    color: white;
    text-decoration: none;

    width: fit-content;
  }
  .btn-div-news:hover {
    color: rgb(61, 60, 71);
    background-color: white;
    transition: 0.3s all ease-in-out;
  }
  .btn-div-news:hover > a {
    color: rgb(61, 60, 71);
    transition: 0.3s all ease-in-out;
  }
  .btn:hover {
    transform: translateY(-5px);
  }
  .btn-div-news {
    border-color: rgb(61, 60, 71);
    background-color: rgb(61, 60, 71);
    width: auto;
    display: inline-block;
    transition: 0.3s all ease-in-out;
  }
  hr {
    margin: 20px 10%;
  }
  .first-featurette-news {
    width: 80%;
    margin-left: 10%;
    height: 500px;
  }
  .ffn-content {
    display: flex;
    align-items: center;
    width: 50%;
  }
  .ffn-image {
    width: 500px;
    height: 500px;
  }
  .upper-footer {
    width: 100%;
    height: 35px;
  }
  .footer-item {
    margin: 5px 20px;
    padding: 4px;
  }
  .lower-footer {
    width: 100%;
    height: 35px;
  }
  .copyright {
    text-align: center;
  }
  .slider {
    transition: 0.3s all ease;
  }
</style>
