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
  let sliderLength = 0;
  let sliderAsync = [];
  let files;

  function updateSlider() {
    sliderLength = sliderAsync.length;
    let body = [];
    let bd = new FormData();
    for (let i = 0; i < sliderLength; i++) {
      let sliderCard = document.querySelectorAll(`.slider${i}`);
      let obj = {};

      if (sliderCard[2].files.length > 0) {
        console.log(sliderCard[2].files[0]);
        bd.append("file", sliderCard[2].files[0], String(i));
      } else {
        obj.url = "DEFAULT";
      }
      obj.label = sliderCard[0].value;
      obj.text = sliderCard[1].value;
      body.push(obj);
    }
    console.log(bd);
    bd.forEach(function (value, key) {
      console.log(value);
      console.log(key);
    });
    const headers = { "Content-Type": "application/json" };
    body = JSON.stringify(body);
    fetch("/uploadSlider", { method: "post", bd, headers }) // fetch
      .then((response) => response.json())
      .then(
        (data) => console.log(data) // dane odpowiedzi z serwera
      )
      .catch((error) => console.log(error));
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
          <div class="line">Themes</div>
        </div>
      {:else if selectedTab == "slider"}
        <div use:sliderLoad class="settings flex">
          <!-- SLIDER EDYCJA -->
          <!-- <form
            action="/uploadSlider"
            enctype="multipart/form-data"
            method="post"
          >
            <h1>test</h1>
            <input type="file" name="plik" id="" />
            <button type="submit">submit</button>

            <hr />
          </form> -->
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
                      <a href={item.src}>Link to current picture</a>
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
                  <hr />
                {/each}
                <hr class="sliderHR" />
                <input type="hidden" name="length" value={slider.length} />
                <button type="submit" class="btn btn-save">Save</button>
              </form>
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
    width: 60%;
    position: relative;
    margin-left: calc(50vw - 30%);
    margin-top: calc(50vh - 250px);
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
    justify-content: space-around;
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
  }

  .sliderHR {
    margin: 20px;
    margin-top: 50px;
  }
</style>
