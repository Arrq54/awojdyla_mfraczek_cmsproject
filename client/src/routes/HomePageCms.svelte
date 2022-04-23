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
      actualSliderSide = dataFromDatabase.slider.length - 1;
    } else if (
      actualSliderSide == dataFromDatabase.slider.length - 1 &&
      x == 1
    ) {
      actualSliderSide = 0;
    } else {
      actualSliderSide += x;
    }
  }
  let logged = getLoginStatus();
  async function getLoginStatus() {
    let temp = fetch("/checkLoginStatus").then((response) => response.json());
    const res = await temp;
    return res;
  }
  function logout() {
    fetch("/logout")
      .then((response) => response.fjson())
      .then((data) => (logged = data));
  }
  function settingsMenu() {
    sessionStorage.setItem("selectedTab", "themes");
    window.location.replace("/#/configurationuser");
    location.reload();
  }
  window.onload = () => {
    getSettings();
  };

  let menuOn = true,
    sliderOn = true,
    ffnOn = true,
    newsOn = true;
  async function getSettings() {
    let settings = await fetch("/getSettings").then((response) =>
      response.json()
    );
    console.log(settings.fonts);
    var r = document.querySelector(":root");

    r.style.setProperty(
      "--body-backround-color",
      settings["colors"]["body-background-color"]
    );
    r.style.setProperty(
      "--slider-font-color",
      settings["colors"]["slider-font-color"]
    );
    r.style.setProperty(
      "--news-border-color",
      settings["colors"]["news-border-color"]
    );
    r.style.setProperty(
      "--news-background-color",
      settings["colors"]["news-background-color"]
    );
    r.style.setProperty(
      "--news-header-background-color",
      settings["colors"]["news-header-background-color"]
    );
    r.style.setProperty(
      "--btn-news-background-color",
      settings["colors"]["btn-news-background-color"]
    );
    r.style.setProperty(
      "--news-border-color",
      settings["colors"]["news-border-color"]
    );
    r.style.setProperty("--font-family", `${settings.fonts}`);
    settings.blocks.toggle_ffn == "1" ? (ffnOn = true) : (ffnOn = false);
    settings.blocks.toggle_menu == "1" ? (menuOn = true) : (menuOn = false);
    settings.blocks.toggle_news == "1" ? (newsOn = true) : (newsOn = false);
    settings.blocks.toggle_slider == "1"
      ? (sliderOn = true)
      : (sliderOn = false);

    if (settings.blocks.toggle_menu_orientation == "1") {
      r.style.setProperty("--menu-flex-direction", "column");
      r.style.setProperty("--menu-vetical-horizontal", "row");
      r.style.setProperty("--menu-width", "15%");
      r.style.setProperty("--content-width", "85%");
      r.style.setProperty("--menu-border-right", "1px solid #ebebeb");
    } else {
      r.style.setProperty("--menu-flex-direction", "row");
      r.style.setProperty("--menu-vetical-horizontal", "column");
      r.style.setProperty("--menu-width", "100%");
      r.style.setProperty("--content-width", "100%");
      r.style.setProperty("--menu-border-right", "none");
    }
  }
</script>

<svelte:head>
  <link rel="stylesheet" href="../../style/mainPageStylesheet.css" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=Oswald:wght@300&family=Poppins:wght@300&family=Raleway&family=Roboto+Slab:wght@300&family=Work+Sans:wght@349&display=swap"
    rel="stylesheet"
  />
</svelte:head>

{#await promiseData then dataFromDatabase}
  <div class="page">
    <div class="menu">
      <div class="main">
        <!--NAVBAR MENU-->
        {#if menuOn == true}
          <div class="navbar flex justify-space-between vertical">
            <div class="flex vertical">
              <div class="navbar-item">Icon</div>
              <Router>
                {#each dataFromDatabase.navbarItems as item}
                  <div class="navbar-item">
                    <Link to={item[0]}>{item[0]}</Link>
                  </div>
                {/each}
              </Router>
            </div>
            <div class="register-login-buttons flex vertical">
              {#await logged then status}
                {#if status.user > 0}
                  <div class="navbar-item btn  btn-menu">
                    <a href={null} on:click={settingsMenu} class="btn-a">Menu</a
                    >
                  </div>
                  <div class="navbar-item btn btn-logout">
                    <a href={null} on:click={logout} class="btn-a ">Log out</a>
                  </div>
                {:else}
                  <div class="navbar-item btn  btn-login">
                    <a href="/#/login" class="btn-a">Login</a>
                  </div>
                  <div class="navbar-item btn btn-register">
                    <a href="/#/register" class="btn-a ">Register</a>
                  </div>
                {/if}
              {/await}
            </div>
          </div>
        {/if}
      </div>
    </div>
    <div class="content">
      <!--SLIDER to do-->
      {#if sliderOn}
        <div
          class="slider"
          style="background-image: url({dataFromDatabase.slider[
            actualSliderSide
          ].src});"
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
      {/if}
      {#if newsOn}
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
      {/if}
      {#if ffnOn}
        <div class="first-featurette-news flex justify-space-between">
          <div class="ffn-content">
            <div>
              <h3>{dataFromDatabase.firstFeaturetteNews[0].title}</h3>
              <p>{dataFromDatabase.firstFeaturetteNews[0].text_content}</p>
            </div>
          </div>
          <div
            class="ffn-image"
            style="background-image: url({dataFromDatabase
              .firstFeaturetteNews[0].src});"
          />
        </div>
        <hr />
      {/if}

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
  </div>
{/await}
