<script defer>
  async function asyncCheckLoginStatus() {
    let temp = fetch("/checkLoginStatus").then((response) => response.json());
    return await temp;
  }
  $: status = asyncCheckLoginStatus();
  $: selectedTab =
    sessionStorage.getItem("selectedTab") == null
      ? "themes"
      : sessionStorage.getItem("selectedTab");

  function setTab(tab) {
    document.getElementById(selectedTab).classList.remove("active");
    selectedTab = tab;
    sessionStorage.setItem("selectedTab", tab);
    document.getElementById(tab).classList.add("active");
  }

  async function sliderLoad() {
    fetch("/getSlider")
      .then((response) => response.json())
      .then((data) => (sliderAsync = data));
  }
  let sliderAsync = [];
  let files;

  async function getUsers() {
    fetch("/getUsers")
      .then((response) => response.json())
      .then((data) => (usersData = data));
  }
  let usersData = [];

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
    let body, headers;
    switch (e) {
      case "gray":
        newColors["body-background-color"] = "#FFFFFF";
        newColors["slider-font-color"] = "#B7B7B7";
        newColors["news-border-color"] = "#ACACAC";
        newColors["news-background-color"] = "#FFFFFF";
        newColors["news-header-background-color"] = "#ECECEC";
        newColors["btn-news-background-color"] = "#3D3C47";
        body = JSON.stringify(newColors);
        headers = { "Content-Type": "application/json" };
        fetch("/saveColors", { method: "post", body, headers });
        break;
      case "green":
        newColors["body-background-color"] = "#d8f3dc";
        newColors["slider-font-color"] = "#ffffff";
        newColors["news-border-color"] = "#081c15";
        newColors["news-background-color"] = "#f0fff1";
        newColors["news-header-background-color"] = "#dbfeb8";
        newColors["btn-news-background-color"] = "#081c15";
        body = JSON.stringify(newColors);
        headers = { "Content-Type": "application/json" };
        fetch("/saveColors", { method: "post", body, headers });
      case "blue":
        newColors["body-background-color"] = "#caf0f8";
        newColors["slider-font-color"] = "#ffffff";
        newColors["news-border-color"] = "#03045e";
        newColors["news-background-color"] = "#ade8f4";
        newColors["news-header-background-color"] = "#90e0ef";
        newColors["btn-news-background-color"] = "#03045e";
        body = JSON.stringify(newColors);
        headers = { "Content-Type": "application/json" };
        fetch("/saveColors", { method: "post", body, headers });
      default:
        break;
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
    const body = JSON.stringify(temp);
    const headers = { "Content-Type": "application/json" };
    fetch("/changeOrder", { method: "post", body, headers });
  }

  function setFont(x) {
    let temp = { fontFamily: x };
    const body = JSON.stringify(temp);
    const headers = { "Content-Type": "application/json" };
    fetch("/saveFont", { method: "post", body, headers });
  }

  function toggle(e) {
    console.log(e.target.id);
    let temp = { id: e.target.id, value: e.target.checked };
    const body = JSON.stringify(temp);
    const headers = { "Content-Type": "application/json" };
    fetch("/changeBlockSettings", { method: "post", body, headers });
  }

  async function setFirstTab() {
    document.getElementById(selectedTab).classList.add("active");
  }
</script>

<svelte:head>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=Oswald:wght@300&family=Poppins:wght@300&family=Raleway&family=Roboto+Slab:wght@300&family=Work+Sans:wght@349&display=swap"
    rel="stylesheet"
  />
  <link rel="stylesheet" href="../../style/configurationMenu.css" />
</svelte:head>

<!-- svelte-ignore missing-declaration -->
{#await status then user}
  <div use:setFirstTab class="alls">
    <div class="menu">
      <div class="maincard">
        <ul>
          <li id="themes" on:click={() => setTab("themes")}>Themes</li>
          <li id="slider" on:click={() => setTab("slider")}>Slider</li>
          <li id="menu" on:click={() => setTab("menu")}>Menu</li>
          <li id="users" on:click={() => setTab("users")}>Users</li>
          <li id="articles" on:click={() => setTab("articles")}>Articles</li>
          <li id="pictures" on:click={() => setTab("pictures")}>Pictures</li>
          <li
            id="showSite"
            on:click={() => {
              window.open("/", "_blank");
            }}
          >
            Show the site
          </li>
        </ul>
        {#if user.user == 2}
          <p class="statusAdmin">Admin</p>
        {:else}
          <p class="statusAdmin">No admin permissions</p>
        {/if}
      </div>
    </div>
    <div class="content">
      {#if selectedTab == "themes"}
        <!-- THEMES EDYCJA -->
        <div class="settings">
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
          <div class="card">
            <h3>Select font</h3>
            <div class="fonts flex f-wrap">
              <div
                class="font-showcase"
                on:click={() => setFont("'Poppins', sans-serif")}
              >
                <div style="font-family: Poppins, sans-serif">
                  <h3>Poppins</h3>
                  Lorem ipsum dolor, sit amet consectetur adipisicing elit. Reiciendis
                  atque quod, facere commodi quae nobis magni laboriosam deleniti
                  earum esse impedit cumque ab a dolore veritatis porro vitae fugiat
                  quis!
                </div>
              </div>
              <div
                class="font-showcase"
                on:click={() => setFont("'Oswald', sans-serif")}
              >
                <div style="font-family: Oswald, sans-serif">
                  <h3>Oswald</h3>
                  Lorem ipsum dolor, sit amet consectetur adipisicing elit. Reiciendis
                  atque quod, facere commodi quae nobis magni laboriosam deleniti
                  earum esse impedit cumque ab a dolore veritatis porro vitae fugiat
                  quis!
                </div>
              </div>
              <div
                class="font-showcase"
                on:click={() => setFont("'Raleway', sans-serif")}
              >
                <div style="font-family: Raleway, sans-serif">
                  <h3>Raleway</h3>
                  Lorem ipsum dolor, sit amet consectetur adipisicing elit. Reiciendis
                  atque quod, facere commodi quae nobis magni laboriosam deleniti
                  earum esse impedit cumque ab a dolore veritatis porro vitae fugiat
                  quis!
                </div>
              </div>
              <div
                class="font-showcase"
                on:click={() => setFont("'Roboto Slab', serif")}
              >
                <div style="font-family: Roboto Slab, serif">
                  <h3>Roboto Slab</h3>
                  Lorem ipsum dolor, sit amet consectetur adipisicing elit. Reiciendis
                  atque quod, facere commodi quae nobis magni laboriosam deleniti
                  earum esse impedit cumque ab a dolore veritatis porro vitae fugiat
                  quis!
                </div>
              </div>
              <div
                class="font-showcase"
                on:click={() => setFont("'Work Sans', serif")}
              >
                <div style="font-family: Work Sans, serif">
                  <h3>Work Sans</h3>
                  Lorem ipsum dolor, sit amet consectetur adipisicing elit. Reiciendis
                  atque quod, facere commodi quae nobis magni laboriosam deleniti
                  earum esse impedit cumque ab a dolore veritatis porro vitae fugiat
                  quis!
                </div>
              </div>
            </div>
          </div>
          <div class="card">
            <h3>Site sections/blocks theme</h3>
            <div class="block-theme-section">
              <h4 class="theme-header">Navbar menu</h4>
              <div class="line-theme">
                <div class="title-theme">Menu on/off</div>
                <label class="switch">
                  <input
                    type="checkbox"
                    id="toggle_menu"
                    on:input={(e) => toggle(e)}
                  />
                  <span class="slider round" />
                </label>
              </div>
              <div class="line-theme">
                <div class="title-theme">Menu Vertical (Off - horizontal)</div>
                <label class="switch">
                  <input
                    type="checkbox"
                    id="toggle_menu_orientation"
                    on:input={(e) => toggle(e)}
                  />
                  <span class="slider round" />
                </label>
              </div>
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
                <button type="submit" class="btn btn-save">Save</button>
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
      {:else if selectedTab == "users"}
        <div use:getUsers class="card users">
          {#await usersData then users}
            {#each users as item, i}
              <div class="userCard">
                <img
                  src="./images/avatar.png"
                  alt="avatar"
                  width="200px"
                  height="200px"
                />
                <h3>{item.username}</h3>
                <p>email: {item.email}</p>
                <p>password: <i>{item.password}</i></p>
                <button
                  on:click={() => {
                    EditUser(item.id);
                  }}
                  class="buttonUs btnEdit">Edit</button
                ><br />
                <button
                  on:click={() => {
                    DeleteUser(item.id);
                  }}
                  class="buttonUs btnDelete">Delete</button
                >
              </div>
            {/each}
          {/await}
        </div>
      {/if}
    </div>
  </div>
{/await}

<style>
  @import url("https://fonts.googleapis.com/css?family=Roboto");
  #showSite {
    margin-top: 40px;
  }
  #showSite:hover {
    color: rgb(210, 255, 229);
    background-color: #16a060;
    text-decoration: underline;
    transform: scale(1.1);
    transform: translateX(3%);
    font-size: 22px;
  }
  .buttonUs {
    margin-top: 10px;
    width: 120px;
    height: 32px;
    border: none;
    border-radius: 2px;
    color: #fff;
    font-weight: 500;
    transition: 0.1s ease;
    cursor: pointer;
  }
  .btnEdit {
    background-color: #88aaf5;
  }
  .btnDelete {
    background-color: #e64141c0;
  }
  .buttonUs:hover {
    transform: scale(1.1);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
  }
  .userCard:hover {
    transform: scale(1.1);
    box-shadow: 0 8px 14px rgba(0, 0, 0, 0.4);
  }
  .userCard > p {
    font-size: 15px;
    color: black;
    margin: 0;
    opacity: 100%;
  }
  .users {
    padding: 20px;
    display: flex;
    align-items: start;
    flex-wrap: wrap;
  }
  .userCard {
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.4);
    transition: 0.1s ease;
    text-align: center;
    overflow: hidden;
    width: 240px;
    height: 380px;
    border-radius: 20px;
    margin: 30px;

    background: rgb(183, 228, 199);
    background: linear-gradient(
      180deg,
      rgba(183, 228, 199, 1) 0%,
      rgba(183, 228, 199, 0.41780462184873945) 100%
    );
  }
  .alls {
    width: 100%;
    height: 100%;
    background-color: whitesmoke;
    overflow: auto;
    margin: 0;
  }
  p {
    color: rgb(210, 255, 229);
    margin-bottom: 25px;
    margin-top: 80%;
    margin-left: 15%;
    font-size: 14px;
    opacity: 60%;
  }
  .menu {
    overflow: hidden;
    width: 15%;
    height: 100%;
    padding: 0px;
    background-color: #16a060;
    margin: 0px;
    top: 0;
    position: absolute;
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
    width: 85%;
    height: 100vh;
    padding: 0px;
    margin-left: 15%;
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
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  .statusAdmin {
    position: absolute;
    bottom: 10px;
    left: 25px;
    font-size: 18px;
  }
  .font-showcase {
    padding: 20px;
    margin: 10px;
    width: 350px;
    transition: 0.3s all ease;
    cursor: pointer;
    margin: 5px;
    background-repeat: no-repeat;
    box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;
    background-size: 100% 100%;
  }
  .font-showcase:hover {
    width: 370px;
    transform: translateX(10px);
    transform: translateY(5px);
    transition: 0.3s all ease;
    box-shadow: rgba(0, 0, 0, 0.55) 0px 15px 25px;
  }
  .fonts {
    padding: 15px;
    margin-bottom: 30px;
  }
  .active {
    background-color: #3b8d67b0;
    font-weight: 500;
  }
</style>
