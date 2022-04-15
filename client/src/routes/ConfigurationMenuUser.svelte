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
    let tempList = [...sliderAsync, placeHolder];
    sliderAsync = tempList;
  }
  function removeCard(i) {
    if (confirm(`Do you want to remove slider card nr ${i}?`)) {
      sliderAsync = [...sliderAsync.filter((item, index) => index !== i)];
    }
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
                style="background-image: url(../../images/colorPalette/greenPalette.png);"
              />
              <div
                class="color-palette"
                style="background-image: url(../../images/colorPalette/bluePallette.png);"
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
                      Picture<br />
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
                {/each}
                <hr class="sliderHR" />
                <input type="hidden" name="length" value={slider.length} />
                <button type="submit" class="btn btn-save">Save</button>
              </form>
              <button on:click={addSliderCard}>Add slider card</button>
            {/await}
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
  }
  .color-palette:hover {
    width: 340px;
    height: 110px;
    transition: 0.3s all ease;
  }
  .f-wrap {
    flex-wrap: wrap;
  }
</style>
