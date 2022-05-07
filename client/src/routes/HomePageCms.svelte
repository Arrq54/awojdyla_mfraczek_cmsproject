<script defer>
  import { Router, Link } from "svelte-navigator";
  async function getContentFromDatabase() {
    let temp = fetch("/getContentFromDatabase")
      .then((response) => response.json())
      .then((data) => (dataFromDatabaseSlider = data));
    const res = await temp;
    return res;
  }
  let promiseData = getContentFromDatabase();

  let actualSliderSide = 0;

  function changeSliderSide(x, item) {
    if (actualSliderSide == 0 && x == -1) {
      actualSliderSide = item.content.length - 1;
    } else if (actualSliderSide == item.content.length - 1 && x == 1) {
      actualSliderSide = 0;
    } else {
      actualSliderSide += x;
    }
  }
  let dataFromDatabaseSlider; //slider interval
  let logged = getLoginStatus();
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
      console.log(res);
      return res;
    } else {
      return { permission: -1 };
    }
  }
  function logout() {
    localStorage.removeItem("user");
    window.location.reload();
  }
  function settingsMenu() {
    sessionStorage.setItem("selectedTab", "themes");
    window.location.replace("/#/configurationuser");
    location.reload();
  }
  window.onload = () => {
    getSettings();
    setTimeout(() => {
      setInterval(() => {
        dataFromDatabaseSlider.forEach((element) => {
          if (element.type == "slider") {
            if (actualSliderSide == element.content.length - 1) {
              actualSliderSide = 0;
            } else {
              actualSliderSide += 1;
            }
          }
        });
      }, sliderTimeSpan);
    }, 500);
  };
  let sliderTimeSpan = 0;
  let menuOn = true,
    sliderOn = true,
    ffnOn = true,
    newsOn = true;
  async function getSettings() {
    let settings = await fetch("/getSettings").then((response) =>
      response.json()
    );
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
      r.style.setProperty("--menu-border-bottom", "none");
    } else {
      r.style.setProperty("--menu-flex-direction", "row");
      r.style.setProperty("--menu-vetical-horizontal", "column");
      r.style.setProperty("--menu-width", "100%");
      r.style.setProperty("--content-width", "100%");
      r.style.setProperty("--menu-border-right", "none");
      r.style.setProperty("--menu-border-bottom", "1px solid #ebebeb");
    }
    sliderTimeSpan = settings.sliderTimeSpan;
  }

  function showFilterBox(e) {
    if (document.getElementById("searchBox").style.display == "block")
      document.getElementById("searchBox").style.display = "none";
    if (document.getElementById("sortBox").style.display == "block")
      document.getElementById("sortBox").style.display = "none";
    if (document.getElementById("filterBox").style.display == "none") {
      document.getElementById("filterBox").style.display = "block";
      return;
    }
    document.getElementById("filterBox").style.display = "none";
  }
  let categoryInputs = [];
  function generateCheckboxesForFiltering(node, data) {
    let listOfCategories = [];
    data.forEach((element) => {
      if (!listOfCategories.includes(element.category))
        listOfCategories.push(element.category);
    });

    generateInputs(listOfCategories, data);
  }
  function filterChanged(changed, data) {
    if (changed.checked) {
      categoryInputs.push(changed.value);
    } else {
      categoryInputs = [
        ...categoryInputs.filter((item, index) => item !== changed.value),
      ];
    }
    let filteredNews = [];
    data.forEach((element) => {
      if (categoryInputs.includes(element.category)) {
        filteredNews.push(element);
      }
    });
    let content = dataFromDatabaseSlider;
    content.forEach((element) => {
      if (element.type == "news") {
        element.content = filteredNews;
      }
    });
    promiseData = content;
  }
  function generateInputs(list, data) {
    let parent = document.getElementById("filter-categories");
    list.forEach((element) => {
      let p = document.createElement("div");
      let input = document.createElement("input");
      input.type = "checkbox";
      input.value = element;
      input.checked = true;
      input.oninput = () => filterChanged(input, data);
      let span = document.createElement("span");
      span.innerText = element;
      p.appendChild(input);
      p.appendChild(span);
      parent.appendChild(p);
      categoryInputs.push(element);
    });
  }
  function showSortBox(e) {
    if (document.getElementById("searchBox").style.display == "block")
      document.getElementById("searchBox").style.display = "none";
    if (document.getElementById("filterBox").style.display == "block")
      document.getElementById("filterBox").style.display = "none";
    if (document.getElementById("sortBox").style.display == "none") {
      document.getElementById("sortBox").style.display = "block";
      return;
    }
    document.getElementById("sortBox").style.display = "none";
  }
  function changeSortingOrder(event, data) {
    if (event.target.value == "az") {
      data.sort((a, b) => a.title.localeCompare(b.title));
    } else if (event.target.value == "za") {
      data.sort((a, b) => b.title.localeCompare(a.title));
    }
    let content = dataFromDatabaseSlider;
    content.forEach((element) => {
      if (element.type == "news") {
        element.content = data;
      }
    });
    promiseData = content;
    document.getElementById("sortBox").style.display = "none";
  }
  let copyOfArticles;
  function showSearchBox() {
    if (document.getElementById("filterBox").style.display == "block")
      document.getElementById("filterBox").style.display = "none";
    if (document.getElementById("sortBox").style.display == "block")
      document.getElementById("sortBox").style.display = "none";

    if (document.getElementById("searchBox").style.display == "none") {
      document.getElementById("searchBox").style.display = "block";
      return;
    }
    document.getElementById("searchBox").style.display = "none";
  }

  function searchInArticles(e) {
    let news;
    let temp;

    if (promiseData.length > 0) {
      promiseData.forEach((element) => {
        if (element.type == "news") news = element.content;
      });
      temp = promiseData;
    } else {
      dataFromDatabaseSlider.forEach((element) => {
        if (element.type == "news") news = element.content;
      });
      temp = dataFromDatabaseSlider;
    }
    news.forEach((element) => {
      if (
        element.text_content.includes(e.target.value) == true ||
        element.content.includes(e.target.value) == true
      ) {
        element.disabled = false;
      } else {
        element.disabled = true;
      }
    });
    temp.forEach((element) => {
      if (element.type == "news") element.content = news;
    });
    promiseData = temp;
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
  <div class="flex f-col">
    <div class="page">
      <div class="menu">
        <div class="main">
          <!--NAVBAR MENU-->
          {#if menuOn == true}
            <div class="navbar flex justify-space-between vertical ">
              <div class="flex vertical f-wrap">
                <div class="navbar-item">Icon</div>

                {#each dataFromDatabase[0].content as menuitem}
                  <div class="navbar-item">
                    <a href={`/#/menu/${menuitem[0]}`}>{menuitem[1]}</a>
                  </div>
                {/each}
              </div>
              <div class="register-login-buttons flex vertical">
                {#await logged then status}
                  {#if status.permission >= 0}
                    <div class="navbar-item btn  btn-menu">
                      <a href={null} on:click={settingsMenu} class="btn-a"
                        >Menu</a
                      >
                    </div>
                    <div class="navbar-item btn btn-logout">
                      <a href={null} on:click={logout} class="btn-a ">Log out</a
                      >
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
        {#each dataFromDatabase as item}
          <!--SLIDER to do-->
          {#if item.type == "slider"}
            {#if sliderOn}
              <div
                class="slider"
                style="background-image: url({item.content[actualSliderSide]
                  .src});"
              >
                <div
                  class="arrow arrow-left"
                  on:click={() => changeSliderSide(-1, item)}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512"
                    ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                      d="M224 480c-8.188 0-16.38-3.125-22.62-9.375l-192-192c-12.5-12.5-12.5-32.75 0-45.25l192-192c12.5-12.5 32.75-12.5 45.25 0s12.5 32.75 0 45.25L77.25 256l169.4 169.4c12.5 12.5 12.5 32.75 0 45.25C240.4 476.9 232.2 480 224 480z"
                    /></svg
                  >
                </div>
                <div
                  class="arrow arrow-right"
                  on:click={() => changeSliderSide(1, item)}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512"
                    ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                      d="M96 480c-8.188 0-16.38-3.125-22.62-9.375c-12.5-12.5-12.5-32.75 0-45.25L242.8 256L73.38 86.63c-12.5-12.5-12.5-32.75 0-45.25s32.75-12.5 45.25 0l192 192c12.5 12.5 12.5 32.75 0 45.25l-192 192C112.4 476.9 104.2 480 96 480z"
                    /></svg
                  >
                </div>
                <div class="slider-content">
                  <h4 class="slider-label">
                    {item.content[actualSliderSide].label}
                  </h4>
                  <p class="slider-p">{item.content[actualSliderSide].texts}</p>
                </div>
              </div>
            {/if}
          {:else if item.type == "news"}
            {#if newsOn}
              <div class="buttons-filter-search-sort">
                <div class="filterBox" id="filterBox" style="display: none;">
                  <div class="filter-header">
                    <h5>Filter by categories:</h5>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      PYCH
                      viewBox="0 0 384 512"
                      on:click={(e) => showFilterBox(e)}
                      style="width: 20px; height: 20px; fill: rgb(43, 43, 43); cursor: pointer;"
                      ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                        d="M376.6 427.5c11.31 13.58 9.484 33.75-4.094 45.06c-5.984 4.984-13.25 7.422-20.47 7.422c-9.172 0-18.27-3.922-24.59-11.52L192 305.1l-135.4 162.5c-6.328 7.594-15.42 11.52-24.59 11.52c-7.219 0-14.48-2.438-20.47-7.422c-13.58-11.31-15.41-31.48-4.094-45.06l142.9-171.5L7.422 84.5C-3.891 70.92-2.063 50.75 11.52 39.44c13.56-11.34 33.73-9.516 45.06 4.094L192 206l135.4-162.5c11.3-13.58 31.48-15.42 45.06-4.094c13.58 11.31 15.41 31.48 4.094 45.06l-142.9 171.5L376.6 427.5z"
                      /></svg
                    >
                  </div>
                  <div
                    class="filter-categories"
                    id="filter-categories"
                    use:generateCheckboxesForFiltering={item.content}
                  />
                </div>
                <div class="searchBox" id="searchBox" style="display: none;">
                  <div class="filter-header">
                    <h5>Search:</h5>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 384 512"
                      on:click={(e) => showSearchBox(e)}
                      style="width: 20px; height: 20px; fill: rgb(43, 43, 43); cursor: pointer;"
                      ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                        d="M376.6 427.5c11.31 13.58 9.484 33.75-4.094 45.06c-5.984 4.984-13.25 7.422-20.47 7.422c-9.172 0-18.27-3.922-24.59-11.52L192 305.1l-135.4 162.5c-6.328 7.594-15.42 11.52-24.59 11.52c-7.219 0-14.48-2.438-20.47-7.422c-13.58-11.31-15.41-31.48-4.094-45.06l142.9-171.5L7.422 84.5C-3.891 70.92-2.063 50.75 11.52 39.44c13.56-11.34 33.73-9.516 45.06 4.094L192 206l135.4-162.5c11.3-13.58 31.48-15.42 45.06-4.094c13.58 11.31 15.41 31.48 4.094 45.06l-142.9 171.5L376.6 427.5z"
                      /></svg
                    >
                  </div>
                  <div class="search-field">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 512 512"
                      style="width: 25px; height: 25px"
                      ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                        d="M500.3 443.7l-119.7-119.7c27.22-40.41 40.65-90.9 33.46-144.7C401.8 87.79 326.8 13.32 235.2 1.723C99.01-15.51-15.51 99.01 1.724 235.2c11.6 91.64 86.08 166.7 177.6 178.9c53.8 7.189 104.3-6.236 144.7-33.46l119.7 119.7c15.62 15.62 40.95 15.62 56.57 0C515.9 484.7 515.9 459.3 500.3 443.7zM79.1 208c0-70.58 57.42-128 128-128s128 57.42 128 128c0 70.58-57.42 128-128 128S79.1 278.6 79.1 208z"
                      /></svg
                    >
                    <input
                      type="text"
                      class="search-input"
                      on:input={(e) => searchInArticles(e)}
                    />
                  </div>
                </div>

                <div class="sortBox" id="sortBox" style="display: none;">
                  <div class="sort-header">
                    <h5>Sort:</h5>
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 384 512"
                      on:click={(e) => showSortBox(e)}
                      style="width: 20px; height: 20px; fill: rgb(43, 43, 43); cursor: pointer;"
                      ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                        d="M376.6 427.5c11.31 13.58 9.484 33.75-4.094 45.06c-5.984 4.984-13.25 7.422-20.47 7.422c-9.172 0-18.27-3.922-24.59-11.52L192 305.1l-135.4 162.5c-6.328 7.594-15.42 11.52-24.59 11.52c-7.219 0-14.48-2.438-20.47-7.422c-13.58-11.31-15.41-31.48-4.094-45.06l142.9-171.5L7.422 84.5C-3.891 70.92-2.063 50.75 11.52 39.44c13.56-11.34 33.73-9.516 45.06 4.094L192 206l135.4-162.5c11.3-13.58 31.48-15.42 45.06-4.094c13.58 11.31 15.41 31.48 4.094 45.06l-142.9 171.5L376.6 427.5z"
                      /></svg
                    >
                  </div>
                  <div class="sort-items" id="sort-items">
                    <div class="flex">
                      <input
                        type="radio"
                        name="sorting"
                        id="az"
                        value="az"
                        on:change={(e) => changeSortingOrder(e, item.content)}
                      />
                      <label for="az"
                        ><svg
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 512 512"
                          style="width: 25px; height: 25px"
                          ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                            d="M239.6 373.1c11.94-13.05 11.06-33.31-1.969-45.27c-13.55-12.42-33.76-10.52-45.22 1.973L160 366.1V64.03c0-17.7-14.33-32.03-32-32.03S96 46.33 96 64.03v302l-32.4-35.39C51.64 317.7 31.39 316.7 18.38 328.7c-13.03 11.95-13.9 32.22-1.969 45.27l87.1 96.09c12.12 13.26 35.06 13.26 47.19 0L239.6 373.1zM448 416h-50.75l73.38-73.38c9.156-9.156 11.89-22.91 6.938-34.88S460.9 288 447.1 288H319.1C302.3 288 288 302.3 288 320s14.33 32 32 32h50.75l-73.38 73.38c-9.156 9.156-11.89 22.91-6.938 34.88S307.1 480 319.1 480h127.1C465.7 480 480 465.7 480 448S465.7 416 448 416zM492.6 209.3l-79.99-160.1c-10.84-21.81-46.4-21.81-57.24 0L275.4 209.3c-7.906 15.91-1.5 35.24 14.31 43.19c15.87 7.922 35.04 1.477 42.93-14.4l7.154-14.39h88.43l7.154 14.39c6.174 12.43 23.97 23.87 42.93 14.4C494.1 244.6 500.5 225.2 492.6 209.3zM367.8 167.4L384 134.7l16.22 32.63H367.8z"
                          /></svg
                        ></label
                      >
                    </div>
                    <div class="flex">
                      <input
                        type="radio"
                        name="sorting"
                        id="za"
                        value="za"
                        on:change={(e) => changeSortingOrder(e, item.content)}
                      />
                      <label for="za"
                        ><svg
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 512 512"
                          style="width: 25px; height: 25px"
                          ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                            d="M104.4 470.1c12.12 13.26 35.06 13.26 47.19 0l87.1-96.09c11.94-13.05 11.06-33.31-1.969-45.27c-13.02-11.95-33.27-11.04-45.22 1.973L160 366.1V64.03c0-17.7-14.33-32.03-32-32.03S96 46.33 96 64.03v302l-32.4-35.39c-6.312-6.883-14.94-10.39-23.61-10.39c-7.719 0-15.47 2.785-21.61 8.414c-13.03 11.95-13.9 32.22-1.969 45.27L104.4 470.1zM320 96h50.75l-73.38 73.38c-9.156 9.156-11.89 22.91-6.938 34.88s16.63 19.74 29.56 19.74h127.1C465.7 223.1 480 209.7 480 192s-14.33-32-32-32h-50.75l73.38-73.38c9.156-9.156 11.89-22.91 6.938-34.88S460.9 32 447.1 32h-127.1C302.3 32 288 46.31 288 64S302.3 96 320 96zM492.6 433.3l-79.99-160.1c-10.84-21.81-46.4-21.81-57.24 0l-79.99 160.1c-7.906 15.91-1.5 35.24 14.31 43.19c15.87 7.922 35.04 1.477 42.93-14.4l7.154-14.39h88.43l7.154 14.39c6.174 12.43 23.97 23.87 42.93 14.4C494.1 468.6 500.5 449.2 492.6 433.3zM367.8 391.4L384 358.7l16.22 32.63H367.8z"
                          /></svg
                        ></label
                      >
                    </div>
                  </div>
                </div>

                <div
                  class="filter-btn filter"
                  id="filter"
                  on:click={(e) => showFilterBox(e)}
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 512 512"
                    class="filter-icon"
                    ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                      d="M3.853 54.87C10.47 40.9 24.54 32 40 32H472C487.5 32 501.5 40.9 508.1 54.87C514.8 68.84 512.7 85.37 502.1 97.33L320 320.9V448C320 460.1 313.2 471.2 302.3 476.6C291.5 482 278.5 480.9 268.8 473.6L204.8 425.6C196.7 419.6 192 410.1 192 400V320.9L9.042 97.33C-.745 85.37-2.765 68.84 3.854 54.87L3.853 54.87z"
                    /></svg
                  >
                  <span id="filterSpan">Filter</span>
                </div>

                <div
                  class="filter-btn sort"
                  id="sort"
                  on:click={(e) => showSortBox(e)}
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 320 512"
                    class="filter-icon"
                    ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                      d="M27.66 224h264.7c24.6 0 36.89-29.78 19.54-47.12l-132.3-136.8c-5.406-5.406-12.47-8.107-19.53-8.107c-7.055 0-14.09 2.701-19.45 8.107L8.119 176.9C-9.229 194.2 3.055 224 27.66 224zM292.3 288H27.66c-24.6 0-36.89 29.77-19.54 47.12l132.5 136.8C145.9 477.3 152.1 480 160 480c7.053 0 14.12-2.703 19.53-8.109l132.3-136.8C329.2 317.8 316.9 288 292.3 288z"
                    /></svg
                  >
                  <span id="sortSpan">Sort</span>
                </div>
                <div
                  class="filter-btn search"
                  id="search"
                  on:click={(e) => showSearchBox(e)}
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 512 512"
                    class="filter-icon"
                    ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                      d="M500.3 443.7l-119.7-119.7c27.22-40.41 40.65-90.9 33.46-144.7C401.8 87.79 326.8 13.32 235.2 1.723C99.01-15.51-15.51 99.01 1.724 235.2c11.6 91.64 86.08 166.7 177.6 178.9c53.8 7.189 104.3-6.236 144.7-33.46l119.7 119.7c15.62 15.62 40.95 15.62 56.57 0C515.9 484.7 515.9 459.3 500.3 443.7zM79.1 208c0-70.58 57.42-128 128-128s128 57.42 128 128c0 70.58-57.42 128-128 128S79.1 278.6 79.1 208z"
                    /></svg
                  >
                  <span id="searchSpan">Search</span>
                </div>
              </div>
              <div class="flex justify-content-center news flex-wrap">
                {#each item.content as news}
                  {#if news.disabled != true}
                    <div class="newsBlock">
                      <div class="news-header">
                        <span>{news.header}</span>
                        {#if news.category == "Sport"}
                          <span class="homepage-category sport"
                            ><svg
                              xmlns="http://www.w3.org/2000/svg"
                              viewBox="0 0 512 512"
                              ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                                d="M148.7 171.3L64.21 86.83c-28.39 32.16-48.9 71.38-58.3 114.8C19.41 205.4 33.34 208 48 208C86.34 208 121.1 193.9 148.7 171.3zM194.5 171.9L256 233.4l169.2-169.2C380 24.37 320.9 0 256 0C248.6 0 241.2 .4922 233.1 1.113C237.8 16.15 240 31.8 240 48C240 95.19 222.8 138.4 194.5 171.9zM208 48c0-14.66-2.623-28.59-6.334-42.09C158.2 15.31 118.1 35.82 86.83 64.21l84.48 84.48C193.9 121.1 208 86.34 208 48zM171.9 194.5C138.4 222.8 95.19 240 48 240c-16.2 0-31.85-2.236-46.89-6.031C.4922 241.2 0 248.6 0 256c0 64.93 24.37 124 64.21 169.2L233.4 256L171.9 194.5zM317.5 340.1L256 278.6l-169.2 169.2C131.1 487.6 191.1 512 256 512c7.438 0 14.75-.4922 22.03-1.113C274.2 495.8 272 480.2 272 464C272 416.8 289.2 373.6 317.5 340.1zM363.3 340.7l84.48 84.48c28.39-32.16 48.9-71.38 58.3-114.8C492.6 306.6 478.7 304 464 304C425.7 304 390.9 318.1 363.3 340.7zM447.8 86.83L278.6 256l61.52 61.52C373.6 289.2 416.8 272 464 272c16.2 0 31.85 2.236 46.89 6.031C511.5 270.8 512 263.4 512 256C512 191.1 487.6 131.1 447.8 86.83zM304 464c0 14.66 2.623 28.59 6.334 42.09c43.46-9.4 82.67-29.91 114.8-58.3l-84.48-84.48C318.1 390.9 304 425.7 304 464z"
                              /></svg
                            >
                            {news.category}</span
                          >
                        {:else if news.category == "Fashion"}
                          <span class="homepage-category fashion"
                            ><svg
                              xmlns="http://www.w3.org/2000/svg"
                              viewBox="0 0 640 512"
                              ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                                d="M640 162.8c0 6.917-2.293 13.88-7.012 19.7l-49.96 61.63c-6.32 7.796-15.62 11.85-25.01 11.85c-7.01 0-14.07-2.262-19.97-6.919L480 203.3V464c0 26.51-21.49 48-48 48H208C181.5 512 160 490.5 160 464V203.3L101.1 249.1C96.05 253.7 88.99 255.1 81.98 255.1c-9.388 0-18.69-4.057-25.01-11.85L7.012 182.5C2.292 176.7-.0003 169.7-.0003 162.8c0-9.262 4.111-18.44 12.01-24.68l135-106.6C159.8 21.49 175.7 16 191.1 16H225.6C233.3 61.36 272.5 96 320 96s86.73-34.64 94.39-80h33.6c16.35 0 32.22 5.49 44.99 15.57l135 106.6C635.9 144.4 640 153.6 640 162.8z"
                              /></svg
                            >
                            {news.category}</span
                          >
                        {:else if news.category == "Business"}
                          <span class="homepage-category business"
                            ><svg
                              xmlns="http://www.w3.org/2000/svg"
                              viewBox="0 0 512 512"
                              ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                                d="M64 400C64 408.8 71.16 416 80 416H480C497.7 416 512 430.3 512 448C512 465.7 497.7 480 480 480H80C35.82 480 0 444.2 0 400V64C0 46.33 14.33 32 32 32C49.67 32 64 46.33 64 64V400zM342.6 278.6C330.1 291.1 309.9 291.1 297.4 278.6L240 221.3L150.6 310.6C138.1 323.1 117.9 323.1 105.4 310.6C92.88 298.1 92.88 277.9 105.4 265.4L217.4 153.4C229.9 140.9 250.1 140.9 262.6 153.4L320 210.7L425.4 105.4C437.9 92.88 458.1 92.88 470.6 105.4C483.1 117.9 483.1 138.1 470.6 150.6L342.6 278.6z"
                              /></svg
                            >
                            {news.category}</span
                          >
                        {:else if news.category == "Science"}
                          <span class="homepage-category science"
                            ><svg
                              xmlns="http://www.w3.org/2000/svg"
                              viewBox="0 0 448 512"
                              ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                                d="M437.2 403.5L319.1 215L319.1 64h7.1c13.25 0 23.1-10.75 23.1-24l-.0002-16c0-13.25-10.75-24-23.1-24H120C106.8 0 96.01 10.75 96.01 24l-.0002 16c0 13.25 10.75 24 23.1 24h7.1L128 215l-117.2 188.5C-18.48 450.6 15.27 512 70.89 512h306.2C432.7 512 466.5 450.5 437.2 403.5zM137.1 320l48.15-77.63C189.8 237.3 191.9 230.8 191.9 224l.0651-160h63.99l-.06 160c0 6.875 2.25 13.25 5.875 18.38L309.9 320H137.1z"
                              /></svg
                            >
                            {news.category}</span
                          >
                        {:else if news.category == "Technology"}
                          <span class="homepage-category tech"
                            ><svg
                              xmlns="http://www.w3.org/2000/svg"
                              viewBox="0 0 576 512"
                              ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                                d="M528 0h-480C21.5 0 0 21.5 0 48v320C0 394.5 21.5 416 48 416h192L224 464H152C138.8 464 128 474.8 128 488S138.8 512 152 512h272c13.25 0 24-10.75 24-24s-10.75-24-24-24H352L336 416h192c26.5 0 48-21.5 48-48v-320C576 21.5 554.5 0 528 0zM512 288H64V64h448V288z"
                              /></svg
                            >
                            {news.category}</span
                          >
                        {:else if news.category == "Art & Culture"}
                          <span class="homepage-category art"
                            ><svg
                              xmlns="http://www.w3.org/2000/svg"
                              viewBox="0 0 384 512"
                              ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                                d="M224 0H336C362.5 0 384 21.49 384 48V256H0V48C0 21.49 21.49 0 48 0H64L96 64L128 0H160L192 64L224 0zM384 288V320C384 355.3 355.3 384 320 384H256V448C256 483.3 227.3 512 192 512C156.7 512 128 483.3 128 448V384H64C28.65 384 0 355.3 0 320V288H384zM192 464C200.8 464 208 456.8 208 448C208 439.2 200.8 432 192 432C183.2 432 176 439.2 176 448C176 456.8 183.2 464 192 464z"
                              /></svg
                            >
                            {news.category}</span
                          >
                        {:else if news.category == "Current Affairs"}
                          <span class="homepage-category currentAffairs"
                            ><svg
                              xmlns="http://www.w3.org/2000/svg"
                              viewBox="0 0 512 512"
                              ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                                d="M512 256C512 397.4 397.4 512 256 512C114.6 512 0 397.4 0 256C0 114.6 114.6 0 256 0C397.4 0 512 114.6 512 256zM177.8 63.19L187.8 80.62C190.5 85.46 192 90.93 192 96.5V137.9C192 141.8 193.6 145.6 196.3 148.3C202.6 154.6 212.8 153.1 218.3 147.1L231.9 130.1C236.6 124.2 244.8 122.4 251.6 125.8L266.8 133.4C270.2 135.1 273.1 136 277.8 136C284.3 136 290.6 133.4 295.2 128.8L299.1 124.9C302 121.1 306.5 121.2 310.1 123.1L339.4 137.7C347.1 141.6 352 149.5 352 158.1C352 168.6 344.9 177.8 334.7 180.3L299.3 189.2C291.9 191 284.2 190.7 276.1 188.3L244.1 177.7C241.7 176.6 238.2 176 234.8 176C227.8 176 220.1 178.3 215.4 182.5L176 212C165.9 219.6 160 231.4 160 244V272C160 298.5 181.5 320 208 320H240C248.8 320 256 327.2 256 336V384C256 401.7 270.3 416 288 416C298.1 416 307.6 411.3 313.6 403.2L339.2 369.1C347.5 357.1 352 344.5 352 330.7V318.6C352 314.7 354.6 311.3 358.4 310.4L363.7 309.1C375.6 306.1 384 295.4 384 283.1C384 275.1 381.2 269.2 376.2 264.2L342.7 230.7C338.1 226.1 338.1 221 342.7 217.3C348.4 211.6 356.8 209.6 364.5 212.2L378.6 216.9C390.9 220.1 404.3 215.4 410.1 203.8C413.6 196.8 421.3 193.1 428.1 194.6L456.4 200.1C431.1 112.4 351.5 48 256 48C228.3 48 201.1 53.4 177.8 63.19L177.8 63.19z"
                              /></svg
                            >
                            {news.category}</span
                          >
                        {:else if news.category == "Health & Medicine"}
                          <span class="homepage-category health"
                            ><svg
                              xmlns="http://www.w3.org/2000/svg"
                              viewBox="0 0 512 512"
                              ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                                d="M464 96H384V48C384 21.5 362.5 0 336 0h-160C149.5 0 128 21.5 128 48V96H48C21.5 96 0 117.5 0 144v288C0 458.5 21.5 480 48 480h416c26.5 0 48-21.5 48-48v-288C512 117.5 490.5 96 464 96zM176 48h160V96h-160V48zM368 314c0 8.836-7.164 16-16 16h-54V384c0 8.836-7.164 16-15.1 16h-52c-8.835 0-16-7.164-16-16v-53.1H160c-8.836 0-16-7.164-16-16v-52c0-8.838 7.164-16 16-16h53.1V192c0-8.838 7.165-16 16-16h52c8.836 0 15.1 7.162 15.1 16v54H352c8.836 0 16 7.162 16 16V314z"
                              /></svg
                            >
                            {news.category}</span
                          >
                        {:else if news.category == "Lifestyle"}
                          <span class="homepage-category lifestyle"
                            ><svg
                              xmlns="http://www.w3.org/2000/svg"
                              viewBox="0 0 576 512"
                              ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                                d="M288 0C422.4 0 512 35.2 512 80V128C529.7 128 544 142.3 544 160V224C544 241.7 529.7 256 512 256L512 416C512 433.7 497.7 448 480 448V480C480 497.7 465.7 512 448 512H416C398.3 512 384 497.7 384 480V448H192V480C192 497.7 177.7 512 160 512H128C110.3 512 96 497.7 96 480V448C78.33 448 64 433.7 64 416L64 256C46.33 256 32 241.7 32 224V160C32 142.3 46.33 128 64 128V80C64 35.2 153.6 0 288 0zM128 256C128 273.7 142.3 288 160 288H272V128H160C142.3 128 128 142.3 128 160V256zM304 288H416C433.7 288 448 273.7 448 256V160C448 142.3 433.7 128 416 128H304V288zM144 400C161.7 400 176 385.7 176 368C176 350.3 161.7 336 144 336C126.3 336 112 350.3 112 368C112 385.7 126.3 400 144 400zM432 400C449.7 400 464 385.7 464 368C464 350.3 449.7 336 432 336C414.3 336 400 350.3 400 368C400 385.7 414.3 400 432 400zM368 64H208C199.2 64 192 71.16 192 80C192 88.84 199.2 96 208 96H368C376.8 96 384 88.84 384 80C384 71.16 376.8 64 368 64z"
                              /></svg
                            >
                            {news.category}</span
                          >
                        {:else if news.category == "Law"}
                          <span class="homepage-category law"
                            ><svg
                              xmlns="http://www.w3.org/2000/svg"
                              viewBox="0 0 640 512"
                              ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                                d="M554.9 154.5c-17.62-35.25-68.12-35.38-85.87 0c-87 174.3-84.1 165.9-84.1 181.5c0 44.13 57.25 80 128 80s127.1-35.88 127.1-80C639.1 319.9 641.4 327.3 554.9 154.5zM439.1 320l71.96-144l72.17 144H439.1zM256 336c0-16.12 1.375-8.75-85.12-181.5c-17.62-35.25-68.12-35.38-85.87 0c-87 174.3-84.1 165.9-84.1 181.5c0 44.13 57.25 80 127.1 80S256 380.1 256 336zM127.9 176L200.1 320H55.96L127.9 176zM495.1 448h-143.1V153.3C375.5 143 393.1 121.8 398.4 96h113.6c17.67 0 31.1-14.33 31.1-32s-14.33-32-31.1-32h-128.4c-14.62-19.38-37.5-32-63.62-32S270.1 12.62 256.4 32H128C110.3 32 96 46.33 96 64S110.3 96 127.1 96h113.6c5.25 25.75 22.87 47 46.37 57.25V448H144c-26.51 0-48.01 21.49-48.01 48c0 8.836 7.165 16 16 16h416c8.836 0 16-7.164 16-16C544 469.5 522.5 448 495.1 448z"
                              /></svg
                            >
                            {news.category}</span
                          >
                        {:else}
                          <span class="homepage-category other"
                            ><svg
                              xmlns="http://www.w3.org/2000/svg"
                              viewBox="0 0 512 512"
                              ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                                d="M480 32H128C110.3 32 96 46.33 96 64v336C96 408.8 88.84 416 80 416S64 408.8 64 400V96H32C14.33 96 0 110.3 0 128v288c0 35.35 28.65 64 64 64h384c35.35 0 64-28.65 64-64V64C512 46.33 497.7 32 480 32zM272 416h-96C167.2 416 160 408.8 160 400C160 391.2 167.2 384 176 384h96c8.836 0 16 7.162 16 16C288 408.8 280.8 416 272 416zM272 320h-96C167.2 320 160 312.8 160 304C160 295.2 167.2 288 176 288h96C280.8 288 288 295.2 288 304C288 312.8 280.8 320 272 320zM432 416h-96c-8.836 0-16-7.164-16-16c0-8.838 7.164-16 16-16h96c8.836 0 16 7.162 16 16C448 408.8 440.8 416 432 416zM432 320h-96C327.2 320 320 312.8 320 304C320 295.2 327.2 288 336 288h96C440.8 288 448 295.2 448 304C448 312.8 440.8 320 432 320zM448 208C448 216.8 440.8 224 432 224h-256C167.2 224 160 216.8 160 208v-96C160 103.2 167.2 96 176 96h256C440.8 96 448 103.2 448 112V208z"
                              /></svg
                            >
                            {news.category}</span
                          >
                        {/if}
                      </div>
                      <div class="news-content">
                        <p class="title">{news.title}</p>
                        {news.text_content}
                        <br />
                        <br />
                        <div class="btn-n btn-div-news">
                          <a href={`/#/article/${news.idnews}`} class="btn-news"
                            >{news.button_text}</a
                          >
                        </div>
                      </div>
                    </div>
                  {/if}
                {/each}
              </div>
              <hr />
            {/if}
          {:else if item.type == "firstFeaturetteNews"}
            {#if ffnOn}
              <div class="first-featurette-news flex justify-space-between">
                <div class="ffn-content">
                  <div>
                    <h3>{item.content[0].title}</h3>
                    <p>
                      {item.content[0].text_content}
                    </p>
                  </div>
                </div>
                <div
                  class="ffn-image"
                  style="background-image: url({item.content[0].src});"
                />
              </div>
              <hr />
            {/if}
          {/if}
        {/each}
      </div>
    </div>
    <div class="footer">
      <div class="upper-footer flex justify-content-center f-wrap">
        {#each dataFromDatabase[dataFromDatabase.length - 1].content.links as item}
          <div class="footer-item">
            <a href={`/#/footer/${item[0]}`}>{item[1]}</a>
          </div>
        {/each}
      </div>

      <div class="lower-footer">
        <hr />
        <h4 class="copyright">
          © 2022 {dataFromDatabase[dataFromDatabase.length - 1].content.company}
        </h4>
      </div>
    </div>
  </div>
{/await}
