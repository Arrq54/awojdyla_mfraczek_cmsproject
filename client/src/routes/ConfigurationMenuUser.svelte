<script defer>
  async function asyncCheckLoginStatus() {
    let temp = fetch("/checkLoginStatus").then((response) => response.json());
    return await temp;
  }
  $: status = asyncCheckLoginStatus();
  $: selectedTab = "themes";
  function setTab(tab) {
    selectedTab = tab;
  }

  async function sliderLoad() {
    fetch("/getSlider")
      .then((response) => response.json())
      .then((data) => (sliderAsync = data));
  }
  let sliderAsync = [];
  let files;

  function addSliderCard() {
    console.log(sliderAsync);
    let placeHolder = {};
    placeHolder.src = "../../images/sliderPlaceholder1.png";
    placeHolder.texts = "Placeholder text for new slider card";
    placeHolder.label = "Placeholder label for new slider card";
    placeHolder.sliderOrder = sliderAsync.length;
    let tempList = [...sliderAsync, placeHolder];
    sliderAsync = tempList;
  }
  function removeCard(i) {
    if (confirm(`Do you want to remove slider card nr ${i}?`)) {
      sliderAsync = [...sliderAsync.filter((item, index) => index !== i)];
    }
  }

  function setColor(e) {
    let newColors = {};
    switch (e) {
      case "gray":
        newColors["body-background-color"] = "#FFFFFF";
        newColors["slider-font-color"] = "#B7B7B7";
        newColors["news-border-color"] = "#ACACAC";
        newColors["news-background-color"] = "#FFFFFF";
        newColors["news-header-background-color"] = "#ECECEC";
        newColors["btn-news-background-color"] = "#3D3C47";
        const body = JSON.stringify(newColors);
        const headers = { "Content-Type": "application/json" };
        fetch("/saveColors", { method: "post", body, headers });
    }
  }
  function sliderOrder(type, index, id, list) {
    console.log(type);
    if (type == "up") {
      if (index == list.length - 1) return;
      list[index].sliderOrder += 1;
      list[index + 1].sliderOrder -= 1;
      [list[index], list[index + 1]] = [list[index + 1], list[index]];
      sliderAsync = list;
    } else if (type == "down") {
      if (index == 0) return;
      list[index].sliderOrder -= 1;
      list[index + 1].sliderOrder += 1;
      [list[index], list[index - 1]] = [list[index - 1], list[index]];
      sliderAsync = list;
    }
  }

  function fetchSaveSliderOrder() {
    let temp = { body: sliderAsync };
    const body = JSON.stringify(temp); // body czyli przesyłane na serwer dane
    const headers = { "Content-Type": "application/json" }; // nagłowek czyli typ danych
    fetch("/changeOrder", { method: "post", body, headers }); // fetch
  }
</script>

<div id="backg" />
<!-- svelte-ignore missing-declaration -->
{#await status then user}
  <div class="maincontainer">
    <div class="menu">
      <div class="maincard">
        <ul>
          <li on:click={() => setTab("themes")}>Themes</li>
          <li on:click={() => setTab("slider")}>Slider</li>
          <li on:click={() => setTab("menu")}>Menu</li>
          <li on:click={() => setTab("articles")}>Articles</li>
          <li on:click={() => setTab("pictures")}>Pictures</li>
        </ul>
        {#if user.user == 2}
          <p>Admin</p>
        {:else}
          <p>No admin permissions</p>
        {/if}
      </div>
    </div>
    <div class="content">
      {#if selectedTab == "themes"}
        <!-- THEMES EDYCJA -->
        <div class="settings flex">
          <div class="card">
            <h3>Pick a color theme:</h3>
            <br />
            <div class="flex f-wrap">
              <div
                class="color-palette"
                style="background-image: url(../../images/colorPalette/grayPalette.png);"
                on:click={() => setColor("gray")}
              />
              <div
                class="color-palette"
                style="background-image: url(../../images/colorPalette/greenPalette.png);"
                on:click={() => setColor("green")}
              />
              <div
                class="color-palette"
                style="background-image: url(../../images/colorPalette/bluePalette.png);"
                on:click={() => setColor("blue")}
              />
            </div>
          </div>
        </div>
      {:else if selectedTab == "slider"}
        <div use:sliderLoad class="settings flex">
          <div class="card">
            {#await sliderAsync then slider}
              <form
                action="/uploadSlider"
                enctype="multipart/form-data"
                method="post"
              >
                <button
                  type="button"
                  on:click={() => setTab("changeOrderOfSlider")}
                  >Change order of cards</button
                >
                {#each slider as item, i}
                  <div class="card-header">
                    Slider card nr:{i}
                    <svg
                      class="removeButton"
                      on:click={() => removeCard(i)}
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 448 512"
                      ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                        d="M135.2 17.69C140.6 6.848 151.7 0 163.8 0H284.2C296.3 0 307.4 6.848 312.8 17.69L320 32H416C433.7 32 448 46.33 448 64C448 81.67 433.7 96 416 96H32C14.33 96 0 81.67 0 64C0 46.33 14.33 32 32 32H128L135.2 17.69zM31.1 128H416V448C416 483.3 387.3 512 352 512H95.1C60.65 512 31.1 483.3 31.1 448V128zM111.1 208V432C111.1 440.8 119.2 448 127.1 448C136.8 448 143.1 440.8 143.1 432V208C143.1 199.2 136.8 192 127.1 192C119.2 192 111.1 199.2 111.1 208zM207.1 208V432C207.1 440.8 215.2 448 223.1 448C232.8 448 240 440.8 240 432V208C240 199.2 232.8 192 223.1 192C215.2 192 207.1 199.2 207.1 208zM304 208V432C304 440.8 311.2 448 320 448C328.8 448 336 440.8 336 432V208C336 199.2 328.8 192 320 192C311.2 192 304 199.2 304 208z"
                      /></svg
                    >
                  </div>
                  <div class="line">
                    <h5>Slider label</h5>
                    <input
                      type="text"
                      name={`sliderLabel${i}`}
                      value={item.label}
                      id={`slider${i}`}
                      class={`slider${i}`}
                    />
                  </div>
                  <div class="line">
                    <h5>Slider text</h5>
                    <textarea
                      rows="10"
                      type="text"
                      name={`sliderText${i}`}
                      value={item.texts}
                      id={`slider${i}`}
                      class={`slider${i}`}
                    />
                  </div>
                  <div class="line">
                    <h5>
                      <img src={item.src} alt="" class="showcaseImage" />
                      <input
                        type="hidden"
                        name={`sliderFileName${i}`}
                        value={item.src}
                      />
                    </h5>
                    <input
                      class={`slider${i}`}
                      type="file"
                      name={`sliderFile${i}`}
                      id={`slider${i}`}
                      accept="image/*"
                      bind:files
                    />
                  </div>
                  <input
                    type="hidden"
                    name={`sliderOrder${i}`}
                    value={item.sliderOrder}
                  />
                  <hr class="sliderHR" />
                {/each}

                <input type="hidden" name="length" value={slider.length} />
                <button type="submit" class="btn btn-save">Save</button>
              </form>
              <button on:click={addSliderCard}>Add slider card</button>
            {/await}
          </div>
        </div>
      {:else if selectedTab == "changeOrderOfSlider"}
        <div class="card">
          <!-- MENU EDYCJA -->
          <button on:click={() => setTab("slider")}>Go back</button>
          <button on:click={() => fetchSaveSliderOrder()}>Save</button>
          <div use:sliderLoad class="settings flex">
            <div class="card">
              {#await sliderAsync then slider}
                {#each slider as item, i}
                  <div class="left">
                    <h5>Slider label: {item.label}</h5>
                    <h5>Slider text: {item.texts}</h5>
                    <h5>Photo:</h5>
                    <h5>
                      <img src={item.src} alt="" class="showcaseImage" />
                    </h5>
                  </div>
                  <div class="right">
                    <button
                      on:click={() => sliderOrder("down", i, item.id, slider)}
                    >
                      <svg
                        style="width: 20px; height: 20px"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 384 512"
                        ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                          d="M374.6 246.6C368.4 252.9 360.2 256 352 256s-16.38-3.125-22.62-9.375L224 141.3V448c0 17.69-14.33 31.1-31.1 31.1S160 465.7 160 448V141.3L54.63 246.6c-12.5 12.5-32.75 12.5-45.25 0s-12.5-32.75 0-45.25l160-160c12.5-12.5 32.75-12.5 45.25 0l160 160C387.1 213.9 387.1 234.1 374.6 246.6z"
                        /></svg
                      >
                    </button>
                    <button
                      on:click={() => sliderOrder("up", i, item.id, slider)}
                    >
                      <svg
                        style="width: 20px; height: 20px"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 384 512"
                        ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                          d="M374.6 310.6l-160 160C208.4 476.9 200.2 480 192 480s-16.38-3.125-22.62-9.375l-160-160c-12.5-12.5-12.5-32.75 0-45.25s32.75-12.5 45.25 0L160 370.8V64c0-17.69 14.33-31.1 31.1-31.1S224 46.31 224 64v306.8l105.4-105.4c12.5-12.5 32.75-12.5 45.25 0S387.1 298.1 374.6 310.6z"
                        /></svg
                      >
                    </button>
                  </div>
                  <hr class="sliderHR" />
                {/each}
              {/await}
            </div>
          </div>
        </div>
      {:else if selectedTab == "menu"}
        <div>
          <!-- MENU EDYCJA -->
          menu
        </div>
      {:else if selectedTab == "articles"}
        <!-- ARTICLES EDYCJA -->
        <div>articles</div>
      {:else if selectedTab == "pictures"}
        <!-- Pictures EDYCJA -->
        <div>pictures</div>
      {/if}
    </div>
  </div>
{/await}

<style>
  @import url("https://fonts.googleapis.com/css?family=Roboto");
  p {
    color: rgb(210, 255, 229);
    margin-bottom: 25px;
    margin-top: 80%;
    margin-left: 15%;
    font-size: 14px;
    opacity: 60%;
  }
  .maincontainer {
    width: 80%;
    position: relative;
    margin-left: calc(50vw - 40%);
    margin-top: 200px;
    font-family: "Roboto", sans-serif;
    background: whitesmoke;
    border: 1px solid whitesmoke;
    border-radius: 26px;
    display: flex;
  }
  .menu {
    border: 1px solid #16a060;
    width: 22%;
    padding: 0px;
    background-color: #16a060;
    border-top-left-radius: 25px;
    border-bottom-left-radius: 25px;
  }
  .maincard > ul {
    padding: 0px;
  }
  .maincard li {
    transition: 0.2s all;
    font-size: 19px;
    padding: 22px 10px 15px 30px;
    margin-top: 0px;
    color: rgb(210, 255, 229);
    list-style: none;
  }
  .maincard li:hover {
    color: rgb(90, 1, 179);
    background-color: #81ffc45e;
    cursor: pointer;
  }
  .maincard {
    height: 100%;
    position: relative;
  }
  .content {
    width: 88%;
    height: 100%;
    padding: 0px;
  }
  .flex {
    display: flex;
  }
  .line {
    display: flex;
    justify-content: space-between;
    width: 100%;
  }
  .card {
    position: relative;
    width: 100%;
  }
  .card-header {
    text-align: center;
    font-size: 25px;
    font-weight: bold;
  }
  input[type="text"] {
    width: 400px;
  }
  textarea {
    padding: 0;
    margin: 0;
    resize: none;
    width: 400px;
    height: auto;
  }
  .settings {
    padding: 20px;
    position: relative;
  }

  .sliderHR {
    margin: 20px;
    margin-top: 50px;
  }
  .showcaseImage {
    width: 192px;
    height: 50px;
  }
  .removeButton {
    width: 20px;
    height: 20px;
    margin-left: 30px;
    cursor: pointer;
  }
  .color-palette {
    width: 332px;
    height: 100px;
    transition: 0.3s all ease;
    cursor: pointer;
    margin: 5px;
    background-repeat: no-repeat;
    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
    background-size: 100% 100%;
  }
  .color-palette:hover {
    width: 340px;
    height: 110px;
    transform: translateX(10px);
    transform: translateY(5px);
    transition: 0.3s all ease;
    box-shadow: rgba(0, 0, 0, 0.55) 0px 15px 25px;
  }
  .f-wrap {
    flex-wrap: wrap;
  }
</style>
