<script defer>
  $: status = getLoginStatus();
  $: selectedTab =
    sessionStorage.getItem("selectedTab") == null
      ? "themes"
      : sessionStorage.getItem("selectedTab");

  function setTab(tab) {
    // document.getElementById(selectedTab).classList.remove("active");
    selectedTab = tab;
    sessionStorage.setItem("selectedTab", tab);
    // document.getElementById(tab).classList.add("active");
  }

  async function sliderLoad() {
    fetch("/getSlider")
      .then((response) => response.json())
      .then((data) => (sliderAsync = data));
    let settings = await fetch("/getSettings").then((response) =>
      response.json()
    );
    if (document.querySelector("#slidertime") != null)
      document.querySelector("#slidertime").value = settings.sliderTimeSpan;
    if (document.querySelector("#input-range-value") != null)
      document.querySelector("#input-range-value").innerHTML =
        String(settings.sliderTimeSpan) + " ms";
  }
  async function loadThemes() {
    let settings = await fetch("/getSettings").then((response) =>
      response.json()
    );
    if (settings.blocks.toggle_menu_orientation == "1")
      document.querySelector("#toggle_menu_orientation").checked = true;
    if (settings.blocks.toggle_menu == "1")
      document.querySelector("#toggle_menu").checked = true;
    if (settings.blocks.toggle_slider == "1")
      document.querySelector("#toggle_slider").checked = true;
    if (settings.blocks.toggle_ffn == "1")
      document.querySelector("#toggle_ffn").checked = true;
    if (settings.blocks.toggle_news == "1")
      document.querySelector("#toggle_news").checked = true;
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
    let placeHolder = {};
    placeHolder.src = "../../images/sliderPlaceholder1.png";
    placeHolder.texts = "Placeholder text for new slider card";
    placeHolder.label = "Placeholder label for new slider card";

    placeHolder.sliderOrder = sliderAsync.length;
    let tempList = [...sliderAsync, placeHolder];
    sliderAsync = tempList;
  }

  function removeCard(i, id) {
    if (confirm(`Do you want to remove slider card nr ${i}?`))
      sliderAsync = [...sliderAsync.filter((item, index) => index !== i)];
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
        break;
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
        break;
      default:
        break;
    }
  }
  function sliderOrder(type, index, id, list) {
    if (type == "up") {
      if (index == list.length - 1) return;
      list[index].sliderOrder += 1;
      list[index + 1].sliderOrder -= 1;
      [list[index], list[index + 1]] = [list[index + 1], list[index]];
      sliderAsync = list;
    } else if (type == "down") {
      if (index == 0) return;
      list[index].sliderOrder -= 1;
      list[index - 1].sliderOrder += 1;
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
    let temp = { id: e.target.id, value: e.target.checked };
    const body = JSON.stringify(temp);
    const headers = { "Content-Type": "application/json" };
    fetch("/changeBlockSettings", { method: "post", body, headers });
  }

  async function setFirstTab() {
    // document.getElementById(selectedTab).classList.add("active");
  }

  async function DeleteUser(id) {
    const body = JSON.stringify(id);
    const headers = { "Content-Type": "application/json" };
    fetch("/deleteUser", { method: "post", body, headers });
    window.location.reload();
  }

  async function EditUser(id, username, email, password, admin) {
    if (admin == 2) {
      document.getElementById("edadmin").style.display = "block";
      document.getElementById("ednormal").remove();
      document.getElementById("edImg").src = "./images/admin.png";
    } else {
      document.getElementById("ednormal").style.display = "block";
      document.getElementById("edadmin").remove();
    }
    document.getElementsByName("username")[0].value = username;
    document.getElementsByName("email")[0].value = email;
    document.getElementsByName("password")[0].value = password;

    document.getElementById("saveme").onclick = () => {
      saveme(id);
    };

    let darkDiv = document.createElement("div");
    darkDiv.onclick = goBackEditing;
    darkDiv.style = `position:absolute; width:100%; height:100%; top:0; left:0; background-color:black; z-index:100; opacity:90%;`;
    document.getElementsByClassName("users")[0].append(darkDiv);
    document.getElementsByClassName("users")[0].style.overflow = "hidden";
  }

  async function saveme(id) {
    let username = document.getElementsByName("username")[0].value;
    let email = document.getElementsByName("email")[0].value;
    let password = document.getElementsByName("password")[0].value;
    let permissions = 2;
    if (document.getElementById("permissions") !== null)
      permissions = document.getElementById("permissions").value;
    let canGoFurther = true;
    if (username == "" || email == "" || password == "") canGoFurther = false;
    if (canGoFurther) saveChanges(id, username, email, password, permissions);
    else document.getElementById("err").style.display = "block";
  }

  async function saveChanges(id, username, email, password, permissions) {
    const body = JSON.stringify({
      id: id,
      username: username,
      email: email,
      password: password,
      admin: permissions,
    });
    const headers = { "Content-Type": "application/json" };
    fetch("/editUser", { method: "post", body, headers });
    goBackEditing();
  }

  async function goBackEditing() {
    window.location.reload();
  }

  async function getCurrentSectionOrder() {
    let temp = await fetch("/getCurrentSectionOrder").then((response) =>
      response.json()
    );
    return temp;
  }
  let sectionOrder = getCurrentSectionOrder();
  function changeSectionOrder(i, index, list) {
    if (i == "up") {
      console.log(list);
      list[index].sectionOrder += 1;
      list[index + 1].sectionOrder -= 1;
      [list[index], list[index + 1]] = [list[index + 1], list[index]];
      sectionOrder = list;
    } else if (i == "down") {
      console.log(list);
      list[index].sectionOrder -= 1;
      list[index - 1].sectionOrder += 1;
      [list[index], list[index - 1]] = [list[index - 1], list[index]];
      sectionOrder = list;
    }
  }

  function saveSectionChanges() {
    console.log(sectionOrder.length);
    if (sectionOrder.length != undefined) {
      let temp = { body: sectionOrder };
      const body = JSON.stringify(temp);
      const headers = { "Content-Type": "application/json" };
      fetch("/changeOrderOfSections", { method: "post", body, headers });
    }
  }

  function setSliderTime(e) {
    let value = e.target.value;
    document.querySelector("#input-range-value").innerHTML =
      String(value) + " ms";
  }

  function fetchChangeSliderTime(e) {
    let temp = { body: e.target.value };
    const body = JSON.stringify(temp);
    const headers = { "Content-Type": "application/json" };
    fetch("/updateSliderTime", { method: "post", body, headers });
  }

  let fetchArticles = [];
  async function getArticleData() {
    let data = await fetch("/getNewsToEdit")
      .then((response) => response.json())
      .then((data) => (fetchArticles = data));
  }
  getArticleData();
  function addArticle() {
    let placeHolder = {};
    placeHolder.header = "News placeholder header";
    placeHolder.title = "News title";
    placeHolder.idnews = fetchArticles.length + 1;
    placeHolder.text_content = "Placeholder text for article summary";
    placeHolder.label = "Placeholder label for new slider card";
    placeHolder.button_text = "Placeholder button";
    placeHolder.category = "Placeholder";
    placeHolder.content = "Placeholder for article content";
    placeHolder.newsOrder = fetchArticles.length + 1;
    fetchArticles = [...fetchArticles, placeHolder];
  }
  function removeArticle(i) {
    if (confirm(`Do you want to remove article nr ${i}?`))
      fetchArticles = [...fetchArticles.filter((item, index) => index !== i)];
  }
  function setCurrentCategory(node, obj) {
    let list = document.querySelectorAll(`input[name="category${obj.i}"]`);
    for (let i = 0; i < list.length; i++) {
      let edited = list[i].id.slice(0, -1);
      let category;
      if (obj.category == "Art & Culture") category = "art";
      else if (obj.category == "Health & Medicine") category = "health";
      else if (obj.category == "Current Affairs") category = "currentAffairs";
      else category = obj.category.toLowerCase();
      if (edited == category) {
        list[i].checked = true;
        return;
      }
    }

    for (let i = 0; i < list.length; i++) {
      let edited = list[i].id.slice(0, -1);
      if (edited == "other") {
        list[i].checked = true;
        document.querySelector(`#otherCategory${obj.i}`).style.display =
          "inline-block";
      }
    }
  }
  function checkIfOtherCategory(i, x) {
    if (x == 1) {
      document.querySelector(`#otherCategory${i}`).style.display =
        "inline-block";
    } else {
      document.querySelector(`#otherCategory${i}`).style.display = "none";
    }
  }
  function switchToArticleOrder() {
    selectedTab = "article order";
  }
  async function loadArticles() {
    let temp = await fetch("/getArticles").then((response) => response.json());
    return temp;
  }

  function changeArticleOrder(type, index, list) {
    if (type == "up") {
      if (index == list.length - 1) return;
      list[index].newsOrder = parseInt(list[index].newsOrder) + 1;
      list[index + 1].newsOrder = parseInt(list[index].newsOrder) - 1;
      [list[index], list[index + 1]] = [list[index + 1], list[index]];
      articlesChangeOrder = list;
    } else if (type == "down") {
      if (index == 0) return;
      list[index].newsOrder = parseInt(list[index].newsOrder) - 1;
      list[index - 1].newsOrder = parseInt(list[index].newsOrder) + 1;
      [list[index], list[index - 1]] = [list[index - 1], list[index]];
      articlesChangeOrder = list;
    }
  }
  function fetchSaveArticlesOrder() {
    if (articlesChangeOrder.length > 0) {
      let temp = { body: articlesChangeOrder };
      const body = JSON.stringify(temp);
      const headers = { "Content-Type": "application/json" };
      fetch("/changeOrderOfArticles", { method: "post", body, headers });
    }
  }
  let articlesChangeOrder = loadArticles();

  async function getFfn() {
    let temp = await fetch("/getffn").then((response) => response.json());
    return temp[0];
  }
  let ffn = getFfn();

  async function fetchGetMenuItems() {
    let temp = await fetch("/getMenuItems").then((response) => response.json());
    return temp;
  }

  let fetchMenuItems = fetchGetMenuItems();

  async function fetchGetFooterItems() {
    let temp = await fetch("/getFooterItems").then((response) =>
      response.json()
    );
    return temp;
  }
  let fetchFooterItems = fetchGetFooterItems();

  async function fetchGetFooterCompanyNAme() {
    let temp = await fetch("/getFooterCompany").then((response) =>
      response.json()
    );
    return temp;
  }
  let fetchFooterCompanyName = fetchGetFooterCompanyNAme();

  function addMenuItem(list) {
    let placeHolder = {};
    placeHolder.text_content = "Placeholder";
    placeHolder.content =
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam cursus facilisis arcu, ac ultricies urna sodales et. Vestibulum eget accumsan ipsum, quis fermentum metus. Maecenas aliquam magna nec dui aliquet malesuada. Suspendisse non bibendum tellus. Mauris fringilla, purus ut varius dignissim, dui massa suscipit sem, sed interdum turpis enim et est. Mauris in rutrum felis. Nam eu massa eu nunc vulputate placerat a nec turpis. Morbi quis ante a sapien vestibulum pellentesque. Curabitur quam nibh, maximus sit amet sapien id, faucibus convallis arcu. Etiam non ante commodo augue malesuada posuere non sed ligula. Quisque eros orci, laoreet eget congue egestas, commodo vel eros. Suspendisse eleifend posuere faucibus. Donec ut diam placerat odio congue cursus id eget massa. In pulvinar eros maximus felis elementum, a vehicula neque gravida.\nPellentesque porta eleifend purus, id rutrum nunc convallis id. Nullam tristique lacus augue, ut vehicula tortor facilisis gravida. Nunc placerat elementum elit, sed faucibus risus porta id. Suspendisse convallis neque sed lorem sodales, nec tincidunt felis venenatis. Morbi facilisis metus non enim dictum, ut blandit ex dignissim. Proin vel enim mauris. Aliquam faucibus neque et lacus malesuada, et viverra massa maximus. Aliquam erat volutpat. Morbi eu quam accumsan, luctus neque eu, imperdiet quam. Sed at posuere quam. Praesent eleifend nisl vel convallis sollicitudin. Duis suscipit pretium nunc, sit amet aliquet nulla tempor ut. Nulla sem leo, rutrum id semper ut, efficitur ac quam. Sed placerat, est eu tempus cursus, dolor tortor accumsan felis, nec varius libero dolor nec lacus. Etiam ac volutpat dui, dictum dignissim mauris. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.";

    let tempList = [...list, placeHolder];
    fetchMenuItems = tempList;
  }
  function removeMenuItem(i, list) {
    if (confirm(`Do you want to remove menu item nr ${i}?`))
      fetchMenuItems = [...list.filter((item, index) => index !== i)];
  }
  function addFooterItem(list) {
    let placeHolder = {};
    placeHolder.text_content = "Placeholder";
    placeHolder.content =
      "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam cursus facilisis arcu, ac ultricies urna sodales et. Vestibulum eget accumsan ipsum, quis fermentum metus. Maecenas aliquam magna nec dui aliquet malesuada. Suspendisse non bibendum tellus. Mauris fringilla, purus ut varius dignissim, dui massa suscipit sem, sed interdum turpis enim et est. Mauris in rutrum felis. Nam eu massa eu nunc vulputate placerat a nec turpis. Morbi quis ante a sapien vestibulum pellentesque. Curabitur quam nibh, maximus sit amet sapien id, faucibus convallis arcu. Etiam non ante commodo augue malesuada posuere non sed ligula. Quisque eros orci, laoreet eget congue egestas, commodo vel eros. Suspendisse eleifend posuere faucibus. Donec ut diam placerat odio congue cursus id eget massa. In pulvinar eros maximus felis elementum, a vehicula neque gravida.\nPellentesque porta eleifend purus, id rutrum nunc convallis id. Nullam tristique lacus augue, ut vehicula tortor facilisis gravida. Nunc placerat elementum elit, sed faucibus risus porta id. Suspendisse convallis neque sed lorem sodales, nec tincidunt felis venenatis. Morbi facilisis metus non enim dictum, ut blandit ex dignissim. Proin vel enim mauris. Aliquam faucibus neque et lacus malesuada, et viverra massa maximus. Aliquam erat volutpat. Morbi eu quam accumsan, luctus neque eu, imperdiet quam. Sed at posuere quam. Praesent eleifend nisl vel convallis sollicitudin. Duis suscipit pretium nunc, sit amet aliquet nulla tempor ut. Nulla sem leo, rutrum id semper ut, efficitur ac quam. Sed placerat, est eu tempus cursus, dolor tortor accumsan felis, nec varius libero dolor nec lacus. Etiam ac volutpat dui, dictum dignissim mauris. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.";

    let tempList = [...list, placeHolder];
    fetchFooterItems = tempList;
  }
  function removeFooterItem(i, list) {
    if (confirm(`Do you want to remove footer item nr ${i}?`))
      fetchFooterItems = [...list.filter((item, index) => index !== i)];
  }
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

      sessionStorage.getItem("selectedTab") == null
        ? setTab("themes")
        : setTab(
            sessionStorage.getItem("selectedTab") == "login to customize"
              ? "themes"
              : sessionStorage.getItem("selectedTab")
          );
      return res;
    }
    setTab("login to customize");
    return { permission: -1 };
  }
  async function exportSettings() {
    let exportObject = {};
    let template = await fetch("/getSettings").then((response) =>
      response.json()
    );
    exportObject.template = template;
    let dataFromDatabase = [];
    if (document.querySelector("#database_content").checked == true) {
      dataFromDatabase = await fetch("/getContentFromDatabase").then(
        (response) => response.json()
      );
    }
    exportObject.database = dataFromDatabase;
    let jsonData = JSON.stringify(exportObject);
    var jsonurl =
      "data:text/json;charset=utf-8," + encodeURIComponent(jsonData);
    var a = document.createElement("A");
    a.setAttribute("href", jsonurl);
    a.setAttribute("download", "backup.json");
    a.click();
  }

  async function importFromJSON(input) {
    let text = await input.files[0].text();
    try {
      let importedObject = JSON.parse(text);
      if (importedObject.template != null && importedObject.database != null) {
        console.log(importedObject);
        if (importedObject.database.length == 0) {
          let temp = { body: importedObject.template };
          const body = JSON.stringify(temp);
          const headers = { "Content-Type": "application/json" };
          fetch("/importSettings", { method: "post", body, headers });
        } else {
          let temp = { body: importedObject };
          const body = JSON.stringify(temp);
          const headers = { "Content-Type": "application/json" };
          fetch("/importSettingsWithDatabase", {
            method: "post",
            body,
            headers,
          });
        }
      }
    } catch {
      console.log("not a json file");
    }
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
          {#if user.permission == 2}
            <li id="themes" on:click={() => setTab("themes")}>Themes</li>
            <li id="block_order" on:click={() => setTab("block_order")}>
              Block order
            </li>
            <li id="slider" on:click={() => setTab("slider")}>Slider</li>
            <li id="menu" on:click={() => setTab("menu")}>Menu</li>
            <li id="users" on:click={() => setTab("users")}>Users</li>
            <li id="articles" on:click={() => setTab("articles")}>Articles</li>
            <li id="ffn" on:click={() => setTab("ffn")}>
              First featurette news
            </li>
            <li id="footer" on:click={() => setTab("footer")}>Footer</li>
            <li id="import_export" on:click={() => setTab("import_export")}>
              Import / Export
            </li>
            <li
              id="showSite"
              on:click={() => {
                window.open("/", "_blank");
              }}
            >
              Show the site
            </li>
          {:else if user.permission == 1}
            <li id="themes" on:click={() => setTab("themes")}>Themes</li>
            <li id="block_order" on:click={() => setTab("block_order")}>
              Block order
            </li>
            <li id="slider" on:click={() => setTab("slider")}>Slider</li>
            <li id="menu" on:click={() => setTab("menu")}>Menu</li>
            <li id="articles" on:click={() => setTab("articles")}>Articles</li>
            <li id="ffn" on:click={() => setTab("ffn")}>
              First featurette news
            </li>
            <li id="footer" on:click={() => setTab("footer")}>Footer</li>
            <li id="import_export" on:click={() => setTab("import_export")}>
              Import / Export
            </li>
            <li
              id="showSite"
              on:click={() => {
                window.open("/", "_blank");
              }}
            >
              Show the site
            </li>
          {:else if user.permission == 0}
            <li id="themes" on:click={() => setTab("themes")}>Themes</li>
            <li id="slider" on:click={() => setTab("slider")}>Slider</li>
            <li id="ffn" on:click={() => setTab("ffn")}>
              First featurette news
            </li>
            <li id="import_export" on:click={() => setTab("import_export")}>
              Import / Export
            </li>
            <li
              id="showSite"
              on:click={() => {
                window.open("/", "_blank");
              }}
            >
              Show the site
            </li>
          {:else}
            <li>Login to customize</li>
            <li
              id="showSite"
              on:click={() => {
                window.open("/", "_blank");
              }}
            >
              Show the site
            </li>
          {/if}
        </ul>
        {#if user.permission == 2}
          <p class="statusAdmin">Admin</p>
        {:else if user.permission == 1}
          <p class="statusAdmin">Advanced user permissions</p>
        {:else if user.permission == 0}
          <p class="statusAdmin">Standard user permissions</p>
        {:else}
          <p class="statusAdmin">Access denied</p>
        {/if}
      </div>
    </div>
    <div class="content">
      {#if selectedTab == "themes"}
        <!-- THEMES EDYCJA -->
        <div class="settings" use:loadThemes>
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
              <h4 class="theme-header">Slider</h4>
              <div class="line-theme">
                <div class="title-theme">Slider on/off</div>
                <label class="switch">
                  <input
                    type="checkbox"
                    id="toggle_slider"
                    on:input={(e) => toggle(e)}
                  />
                  <span class="slider round" />
                </label>
              </div>
              <h4 class="theme-header">News</h4>
              <div class="line-theme">
                <div class="title-theme">Important news on/off</div>
                <label class="switch">
                  <input
                    type="checkbox"
                    id="toggle_ffn"
                    on:input={(e) => toggle(e)}
                  />
                  <span class="slider round" />
                </label>
              </div>
              <div class="line-theme">
                <div class="title-theme">News on/off</div>
                <label class="switch">
                  <input
                    type="checkbox"
                    id="toggle_news"
                    on:input={(e) => toggle(e)}
                  />
                  <span class="slider round" />
                </label>
              </div>
            </div>
          </div>
        </div>
      {:else if selectedTab == "block_order"}
        <div>
          <!-- MENU EDYCJA -->
          {#await sectionOrder then order}
            <div class="sections">
              <div class="section-block">Main menu</div>
              <div class="vertical-line" />
              {#each order as itemOrder, i}
                <div class="section-block">
                  {itemOrder.name}
                  {#if i != 0 && i != order.length - 1}
                    <svg
                      on:click={() => changeSectionOrder("down", i, order)}
                      style="width: 20px; height: 20px"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 384 512"
                      ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                        d="M374.6 246.6C368.4 252.9 360.2 256 352 256s-16.38-3.125-22.62-9.375L224 141.3V448c0 17.69-14.33 31.1-31.1 31.1S160 465.7 160 448V141.3L54.63 246.6c-12.5 12.5-32.75 12.5-45.25 0s-12.5-32.75 0-45.25l160-160c12.5-12.5 32.75-12.5 45.25 0l160 160C387.1 213.9 387.1 234.1 374.6 246.6z"
                      /></svg
                    >
                    <svg
                      style="width: 20px; height: 20px"
                      on:click={() => changeSectionOrder("up", i, order)}
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 384 512"
                      ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                        d="M374.6 310.6l-160 160C208.4 476.9 200.2 480 192 480s-16.38-3.125-22.62-9.375l-160-160c-12.5-12.5-12.5-32.75 0-45.25s32.75-12.5 45.25 0L160 370.8V64c0-17.69 14.33-31.1 31.1-31.1S224 46.31 224 64v306.8l105.4-105.4c12.5-12.5 32.75-12.5 45.25 0S387.1 298.1 374.6 310.6z"
                      /></svg
                    >
                  {:else if i == order.length - 1}
                    <svg
                      on:click={() => changeSectionOrder("down", i, order)}
                      style="width: 20px; height: 20px"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 384 512"
                      ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                        d="M374.6 246.6C368.4 252.9 360.2 256 352 256s-16.38-3.125-22.62-9.375L224 141.3V448c0 17.69-14.33 31.1-31.1 31.1S160 465.7 160 448V141.3L54.63 246.6c-12.5 12.5-32.75 12.5-45.25 0s-12.5-32.75 0-45.25l160-160c12.5-12.5 32.75-12.5 45.25 0l160 160C387.1 213.9 387.1 234.1 374.6 246.6z"
                      /></svg
                    >
                  {:else}
                    <svg
                      style="width: 20px; height: 20px"
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 384 512"
                      on:click={() => changeSectionOrder("up", i, order)}
                      ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                        d="M374.6 310.6l-160 160C208.4 476.9 200.2 480 192 480s-16.38-3.125-22.62-9.375l-160-160c-12.5-12.5-12.5-32.75 0-45.25s32.75-12.5 45.25 0L160 370.8V64c0-17.69 14.33-31.1 31.1-31.1S224 46.31 224 64v306.8l105.4-105.4c12.5-12.5 32.75-12.5 45.25 0S387.1 298.1 374.6 310.6z"
                      /></svg
                    >
                  {/if}
                </div>
                <div class="vertical-line" />
              {/each}
              <div class="section-block">Footer</div>
              <button class="button-save" on:click={() => saveSectionChanges()}
                >Save</button
              >
            </div>
          {/await}
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
                <div class="input-range">
                  Slider time span
                  <input
                    type="range"
                    name=""
                    id="slidertime"
                    min="2000"
                    max="10000"
                    step="100"
                    on:input={(e) => setSliderTime(e)}
                    on:change={(e) => fetchChangeSliderTime(e)}
                  />
                  <span id="input-range-value">ms</span>
                </div>
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
                      on:click={() => removeCard(i, item.id)}
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
        <div class="settings">
          <div>
            {#await fetchMenuItems then menuItems}
              <form
                action="/changeMenuItems"
                method="POST"
                enctype="multipart/form-data"
              >
                {#each menuItems as menuItem, i}
                  <div class="card">
                    <div class="line-center">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 448 512"
                        on:click={() => removeMenuItem(i, menuItems)}
                        style="width: 30px; height:30px;"
                        ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                          d="M135.2 17.69C140.6 6.848 151.7 0 163.8 0H284.2C296.3 0 307.4 6.848 312.8 17.69L320 32H416C433.7 32 448 46.33 448 64C448 81.67 433.7 96 416 96H32C14.33 96 0 81.67 0 64C0 46.33 14.33 32 32 32H128L135.2 17.69zM394.8 466.1C393.2 492.3 372.3 512 346.9 512H101.1C75.75 512 54.77 492.3 53.19 466.1L31.1 128H416L394.8 466.1z"
                        /></svg
                      >
                    </div>

                    <div class="line">
                      <h5>On homepage text content</h5>
                      <input
                        type="text"
                        name={`menuTextContent${i}`}
                        value={menuItem.text_content}
                      />
                    </div>
                    <div class="line">
                      <h5>Content of subpage</h5>
                      <input
                        type="text"
                        name={`menuContent${i}`}
                        value={menuItem.content}
                      />
                    </div>
                    <hr class="sliderHR" />
                  </div>
                {/each}

                <input
                  type="hidden"
                  name="menuLength"
                  value={menuItems.length}
                />
                <button type="submit">Save</button>
              </form>
              <button on:click={() => addMenuItem(menuItems)}
                >Add menu item</button
              >
            {/await}
          </div>
        </div>
      {:else if selectedTab == "articles"}
        <!-- ARTICLES EDYCJA -->
        <div class="settings">
          <div class="card" use:getArticleData>
            {#await fetchArticles then articles}
              <form
                method="POST"
                action="/updateArticles"
                enctype="multipart/form-data"
              >
                <button type="submit">Save</button>
                <button on:click={() => switchToArticleOrder()}
                  >Change order of articles</button
                >
                {#each articles as article, i}
                  <div class="card-header">
                    Article, id:{article.idnews}
                    <svg
                      class="removeButton"
                      on:click={() => removeArticle(i)}
                      xmlns="http://www.w3.org/2000/svg"
                      viewBox="0 0 448 512"
                      ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                        d="M135.2 17.69C140.6 6.848 151.7 0 163.8 0H284.2C296.3 0 307.4 6.848 312.8 17.69L320 32H416C433.7 32 448 46.33 448 64C448 81.67 433.7 96 416 96H32C14.33 96 0 81.67 0 64C0 46.33 14.33 32 32 32H128L135.2 17.69zM31.1 128H416V448C416 483.3 387.3 512 352 512H95.1C60.65 512 31.1 483.3 31.1 448V128zM111.1 208V432C111.1 440.8 119.2 448 127.1 448C136.8 448 143.1 440.8 143.1 432V208C143.1 199.2 136.8 192 127.1 192C119.2 192 111.1 199.2 111.1 208zM207.1 208V432C207.1 440.8 215.2 448 223.1 448C232.8 448 240 440.8 240 432V208C240 199.2 232.8 192 223.1 192C215.2 192 207.1 199.2 207.1 208zM304 208V432C304 440.8 311.2 448 320 448C328.8 448 336 440.8 336 432V208C336 199.2 328.8 192 320 192C311.2 192 304 199.2 304 208z"
                      /></svg
                    >
                    <div class="line">
                      <h5>On homepage article Header</h5>
                      <input
                        type="text"
                        class="article-edit mt-5 w-500"
                        name={`articleHeader${i}`}
                        value={article.header}
                        id=""
                      />
                    </div>
                    <div class="line">
                      <h5>Article title</h5>
                      <input
                        type="text"
                        class="article-edit mt-5 w-500"
                        name={`articleTitle${i}`}
                        value={article.title}
                        id=""
                      />
                    </div>
                    <div class="line">
                      <h5>Article summary</h5>
                      <textarea
                        class="article-edit article-textarea mt-5 w-500"
                        name={`articleSummary${i}`}
                        value={article.text_content}
                        id=""
                      />
                    </div>
                    <div class="line">
                      <h5>On button text</h5>
                      <input
                        type="text"
                        class="article-edit  mt-5 w-500"
                        name={`articleButtonText${i}`}
                        value={article.button_text}
                        id=""
                      />
                    </div>
                    <div class="line">
                      <h5>Article text</h5>
                      <textarea
                        type="text"
                        class="article-edit article-text-textarea  mt-5 w-500"
                        name={`articleText${i}`}
                        value={article.content}
                        id=""
                      />
                    </div>

                    <div class="line-evenly">Category {article.category}</div>
                    <div class="categories">
                      <div
                        class="category sport"
                        on:click={() => checkIfOtherCategory(i, 0)}
                      >
                        <input
                          type="radio"
                          name={`category${i}`}
                          id={`sport${i}`}
                          value="Sport"
                        /><label for={`sport${i}`} class="label-category">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512"
                            ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                              d="M148.7 171.3L64.21 86.83c-28.39 32.16-48.9 71.38-58.3 114.8C19.41 205.4 33.34 208 48 208C86.34 208 121.1 193.9 148.7 171.3zM194.5 171.9L256 233.4l169.2-169.2C380 24.37 320.9 0 256 0C248.6 0 241.2 .4922 233.1 1.113C237.8 16.15 240 31.8 240 48C240 95.19 222.8 138.4 194.5 171.9zM208 48c0-14.66-2.623-28.59-6.334-42.09C158.2 15.31 118.1 35.82 86.83 64.21l84.48 84.48C193.9 121.1 208 86.34 208 48zM171.9 194.5C138.4 222.8 95.19 240 48 240c-16.2 0-31.85-2.236-46.89-6.031C.4922 241.2 0 248.6 0 256c0 64.93 24.37 124 64.21 169.2L233.4 256L171.9 194.5zM317.5 340.1L256 278.6l-169.2 169.2C131.1 487.6 191.1 512 256 512c7.438 0 14.75-.4922 22.03-1.113C274.2 495.8 272 480.2 272 464C272 416.8 289.2 373.6 317.5 340.1zM363.3 340.7l84.48 84.48c28.39-32.16 48.9-71.38 58.3-114.8C492.6 306.6 478.7 304 464 304C425.7 304 390.9 318.1 363.3 340.7zM447.8 86.83L278.6 256l61.52 61.52C373.6 289.2 416.8 272 464 272c16.2 0 31.85 2.236 46.89 6.031C511.5 270.8 512 263.4 512 256C512 191.1 487.6 131.1 447.8 86.83zM304 464c0 14.66 2.623 28.59 6.334 42.09c43.46-9.4 82.67-29.91 114.8-58.3l-84.48-84.48C318.1 390.9 304 425.7 304 464z"
                            /></svg
                          >
                          Sport
                        </label>
                      </div>
                      <div
                        class="category fashion"
                        on:click={() => checkIfOtherCategory(i, 0)}
                      >
                        <input
                          type="radio"
                          name={`category${i}`}
                          id={`fashion${i}`}
                          value="Fashion"
                        /><label for={`fashion${i}`} class="label-category">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 640 512"
                            ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                              d="M640 162.8c0 6.917-2.293 13.88-7.012 19.7l-49.96 61.63c-6.32 7.796-15.62 11.85-25.01 11.85c-7.01 0-14.07-2.262-19.97-6.919L480 203.3V464c0 26.51-21.49 48-48 48H208C181.5 512 160 490.5 160 464V203.3L101.1 249.1C96.05 253.7 88.99 255.1 81.98 255.1c-9.388 0-18.69-4.057-25.01-11.85L7.012 182.5C2.292 176.7-.0003 169.7-.0003 162.8c0-9.262 4.111-18.44 12.01-24.68l135-106.6C159.8 21.49 175.7 16 191.1 16H225.6C233.3 61.36 272.5 96 320 96s86.73-34.64 94.39-80h33.6c16.35 0 32.22 5.49 44.99 15.57l135 106.6C635.9 144.4 640 153.6 640 162.8z"
                            /></svg
                          >
                          Fashion
                        </label>
                      </div>

                      <div
                        class="category business"
                        on:click={() => checkIfOtherCategory(i, 0)}
                      >
                        <input
                          type="radio"
                          name={`category${i}`}
                          id={`business${i}`}
                          value="Business"
                        /><label for={`business${i}`} class="label-category">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512"
                            ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                              d="M64 400C64 408.8 71.16 416 80 416H480C497.7 416 512 430.3 512 448C512 465.7 497.7 480 480 480H80C35.82 480 0 444.2 0 400V64C0 46.33 14.33 32 32 32C49.67 32 64 46.33 64 64V400zM342.6 278.6C330.1 291.1 309.9 291.1 297.4 278.6L240 221.3L150.6 310.6C138.1 323.1 117.9 323.1 105.4 310.6C92.88 298.1 92.88 277.9 105.4 265.4L217.4 153.4C229.9 140.9 250.1 140.9 262.6 153.4L320 210.7L425.4 105.4C437.9 92.88 458.1 92.88 470.6 105.4C483.1 117.9 483.1 138.1 470.6 150.6L342.6 278.6z"
                            /></svg
                          >
                          Business
                        </label>
                      </div>
                      <div
                        class="category science"
                        on:click={() => checkIfOtherCategory(i, 0)}
                      >
                        <input
                          type="radio"
                          name={`category${i}`}
                          id={`science${i}`}
                          value="Science"
                        /><label for={`science${i}`} class="label-category">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 448 512"
                            ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                              d="M437.2 403.5L319.1 215L319.1 64h7.1c13.25 0 23.1-10.75 23.1-24l-.0002-16c0-13.25-10.75-24-23.1-24H120C106.8 0 96.01 10.75 96.01 24l-.0002 16c0 13.25 10.75 24 23.1 24h7.1L128 215l-117.2 188.5C-18.48 450.6 15.27 512 70.89 512h306.2C432.7 512 466.5 450.5 437.2 403.5zM137.1 320l48.15-77.63C189.8 237.3 191.9 230.8 191.9 224l.0651-160h63.99l-.06 160c0 6.875 2.25 13.25 5.875 18.38L309.9 320H137.1z"
                            /></svg
                          >
                          Science
                        </label>
                      </div>

                      <div
                        class="category tech"
                        on:click={() => checkIfOtherCategory(i, 0)}
                      >
                        <input
                          type="radio"
                          name={`category${i}`}
                          id={`technology${i}`}
                          value="Technology"
                        /><label for={`technology${i}`} class="label-category">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 576 512"
                            ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                              d="M528 0h-480C21.5 0 0 21.5 0 48v320C0 394.5 21.5 416 48 416h192L224 464H152C138.8 464 128 474.8 128 488S138.8 512 152 512h272c13.25 0 24-10.75 24-24s-10.75-24-24-24H352L336 416h192c26.5 0 48-21.5 48-48v-320C576 21.5 554.5 0 528 0zM512 288H64V64h448V288z"
                            /></svg
                          >
                          Technology
                        </label>
                      </div>
                      <div
                        class="category art"
                        on:click={() => checkIfOtherCategory(i, 0)}
                      >
                        <input
                          type="radio"
                          name={`category${i}`}
                          id={`art${i}`}
                          value="Art & Culture"
                        /><label for={`art${i}`} class="label-category">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 384 512"
                            ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                              d="M224 0H336C362.5 0 384 21.49 384 48V256H0V48C0 21.49 21.49 0 48 0H64L96 64L128 0H160L192 64L224 0zM384 288V320C384 355.3 355.3 384 320 384H256V448C256 483.3 227.3 512 192 512C156.7 512 128 483.3 128 448V384H64C28.65 384 0 355.3 0 320V288H384zM192 464C200.8 464 208 456.8 208 448C208 439.2 200.8 432 192 432C183.2 432 176 439.2 176 448C176 456.8 183.2 464 192 464z"
                            /></svg
                          >
                          Art & Culture
                        </label>
                      </div>
                      <div
                        class="category currentAffairs"
                        on:click={() => checkIfOtherCategory(i, 0)}
                      >
                        <input
                          type="radio"
                          name={`category${i}`}
                          id={`currentAffairs${i}`}
                          value="Current Affairs"
                        /><label
                          for={`currentAffairs${i}`}
                          class="label-category"
                        >
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512"
                            ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                              d="M512 256C512 397.4 397.4 512 256 512C114.6 512 0 397.4 0 256C0 114.6 114.6 0 256 0C397.4 0 512 114.6 512 256zM177.8 63.19L187.8 80.62C190.5 85.46 192 90.93 192 96.5V137.9C192 141.8 193.6 145.6 196.3 148.3C202.6 154.6 212.8 153.1 218.3 147.1L231.9 130.1C236.6 124.2 244.8 122.4 251.6 125.8L266.8 133.4C270.2 135.1 273.1 136 277.8 136C284.3 136 290.6 133.4 295.2 128.8L299.1 124.9C302 121.1 306.5 121.2 310.1 123.1L339.4 137.7C347.1 141.6 352 149.5 352 158.1C352 168.6 344.9 177.8 334.7 180.3L299.3 189.2C291.9 191 284.2 190.7 276.1 188.3L244.1 177.7C241.7 176.6 238.2 176 234.8 176C227.8 176 220.1 178.3 215.4 182.5L176 212C165.9 219.6 160 231.4 160 244V272C160 298.5 181.5 320 208 320H240C248.8 320 256 327.2 256 336V384C256 401.7 270.3 416 288 416C298.1 416 307.6 411.3 313.6 403.2L339.2 369.1C347.5 357.1 352 344.5 352 330.7V318.6C352 314.7 354.6 311.3 358.4 310.4L363.7 309.1C375.6 306.1 384 295.4 384 283.1C384 275.1 381.2 269.2 376.2 264.2L342.7 230.7C338.1 226.1 338.1 221 342.7 217.3C348.4 211.6 356.8 209.6 364.5 212.2L378.6 216.9C390.9 220.1 404.3 215.4 410.1 203.8C413.6 196.8 421.3 193.1 428.1 194.6L456.4 200.1C431.1 112.4 351.5 48 256 48C228.3 48 201.1 53.4 177.8 63.19L177.8 63.19z"
                            /></svg
                          >
                          Current Affairs
                        </label>
                      </div>
                      <div
                        class="category health"
                        on:click={() => checkIfOtherCategory(i, 0)}
                      >
                        <input
                          type="radio"
                          name={`category${i}`}
                          id={`health${i}`}
                          value="Health & Medicine"
                        /><label for={`health${i}`} class="label-category">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512"
                            ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                              d="M464 96H384V48C384 21.5 362.5 0 336 0h-160C149.5 0 128 21.5 128 48V96H48C21.5 96 0 117.5 0 144v288C0 458.5 21.5 480 48 480h416c26.5 0 48-21.5 48-48v-288C512 117.5 490.5 96 464 96zM176 48h160V96h-160V48zM368 314c0 8.836-7.164 16-16 16h-54V384c0 8.836-7.164 16-15.1 16h-52c-8.835 0-16-7.164-16-16v-53.1H160c-8.836 0-16-7.164-16-16v-52c0-8.838 7.164-16 16-16h53.1V192c0-8.838 7.165-16 16-16h52c8.836 0 15.1 7.162 15.1 16v54H352c8.836 0 16 7.162 16 16V314z"
                            /></svg
                          >
                          Health & Medicine
                        </label>
                      </div>
                      <div
                        class="category lifestyle"
                        on:click={() => checkIfOtherCategory(i, 0)}
                      >
                        <input
                          type="radio"
                          name={`category${i}`}
                          id={`lifestyle${i}`}
                          value="Lifestyle"
                        /><label for={`lifestyle${i}`} class="label-category">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 576 512"
                            ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                              d="M288 0C422.4 0 512 35.2 512 80V128C529.7 128 544 142.3 544 160V224C544 241.7 529.7 256 512 256L512 416C512 433.7 497.7 448 480 448V480C480 497.7 465.7 512 448 512H416C398.3 512 384 497.7 384 480V448H192V480C192 497.7 177.7 512 160 512H128C110.3 512 96 497.7 96 480V448C78.33 448 64 433.7 64 416L64 256C46.33 256 32 241.7 32 224V160C32 142.3 46.33 128 64 128V80C64 35.2 153.6 0 288 0zM128 256C128 273.7 142.3 288 160 288H272V128H160C142.3 128 128 142.3 128 160V256zM304 288H416C433.7 288 448 273.7 448 256V160C448 142.3 433.7 128 416 128H304V288zM144 400C161.7 400 176 385.7 176 368C176 350.3 161.7 336 144 336C126.3 336 112 350.3 112 368C112 385.7 126.3 400 144 400zM432 400C449.7 400 464 385.7 464 368C464 350.3 449.7 336 432 336C414.3 336 400 350.3 400 368C400 385.7 414.3 400 432 400zM368 64H208C199.2 64 192 71.16 192 80C192 88.84 199.2 96 208 96H368C376.8 96 384 88.84 384 80C384 71.16 376.8 64 368 64z"
                            /></svg
                          >
                          Lifestyle
                        </label>
                      </div>
                      <div
                        class="category law"
                        on:click={() => checkIfOtherCategory(i, 0)}
                      >
                        <input
                          type="radio"
                          name={`category${i}`}
                          id={`law${i}`}
                          value="Law"
                        /><label for={`law${i}`} class="label-category">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 640 512"
                            ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                              d="M554.9 154.5c-17.62-35.25-68.12-35.38-85.87 0c-87 174.3-84.1 165.9-84.1 181.5c0 44.13 57.25 80 128 80s127.1-35.88 127.1-80C639.1 319.9 641.4 327.3 554.9 154.5zM439.1 320l71.96-144l72.17 144H439.1zM256 336c0-16.12 1.375-8.75-85.12-181.5c-17.62-35.25-68.12-35.38-85.87 0c-87 174.3-84.1 165.9-84.1 181.5c0 44.13 57.25 80 127.1 80S256 380.1 256 336zM127.9 176L200.1 320H55.96L127.9 176zM495.1 448h-143.1V153.3C375.5 143 393.1 121.8 398.4 96h113.6c17.67 0 31.1-14.33 31.1-32s-14.33-32-31.1-32h-128.4c-14.62-19.38-37.5-32-63.62-32S270.1 12.62 256.4 32H128C110.3 32 96 46.33 96 64S110.3 96 127.1 96h113.6c5.25 25.75 22.87 47 46.37 57.25V448H144c-26.51 0-48.01 21.49-48.01 48c0 8.836 7.165 16 16 16h416c8.836 0 16-7.164 16-16C544 469.5 522.5 448 495.1 448z"
                            /></svg
                          >
                          Law
                        </label>
                      </div>
                      <div
                        class="category other"
                        on:click={() => checkIfOtherCategory(i, 1)}
                      >
                        <input
                          type="radio"
                          name={`category${i}`}
                          id={`other${i}`}
                          value="other"
                        /><label for={`other${i}`} class="label-category">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 512 512"
                            ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                              d="M480 32H128C110.3 32 96 46.33 96 64v336C96 408.8 88.84 416 80 416S64 408.8 64 400V96H32C14.33 96 0 110.3 0 128v288c0 35.35 28.65 64 64 64h384c35.35 0 64-28.65 64-64V64C512 46.33 497.7 32 480 32zM272 416h-96C167.2 416 160 408.8 160 400C160 391.2 167.2 384 176 384h96c8.836 0 16 7.162 16 16C288 408.8 280.8 416 272 416zM272 320h-96C167.2 320 160 312.8 160 304C160 295.2 167.2 288 176 288h96C280.8 288 288 295.2 288 304C288 312.8 280.8 320 272 320zM432 416h-96c-8.836 0-16-7.164-16-16c0-8.838 7.164-16 16-16h96c8.836 0 16 7.162 16 16C448 408.8 440.8 416 432 416zM432 320h-96C327.2 320 320 312.8 320 304C320 295.2 327.2 288 336 288h96C440.8 288 448 295.2 448 304C448 312.8 440.8 320 432 320zM448 208C448 216.8 440.8 224 432 224h-256C167.2 224 160 216.8 160 208v-96C160 103.2 167.2 96 176 96h256C440.8 96 448 103.2 448 112V208z"
                            /></svg
                          >
                          Other:
                          <input
                            type="text"
                            class="othercategory"
                            value={article.category}
                            name={`otherCategory${i}`}
                            id={`otherCategory${i}`}
                            style="display: none;"
                          />
                        </label>
                      </div>
                    </div>
                    <input
                      type="hidden"
                      value={article.pictures}
                      name={`articleFiles${i}`}
                    />
                    <div class="line">
                      <input
                        type="file"
                        name={`articleImages${i}`}
                        multiple
                        accept="image/*"
                        id=""
                      />
                    </div>
                  </div>
                  <input
                    type="hidden"
                    name=""
                    value={i}
                    use:setCurrentCategory={{
                      i: i,
                      category: article.category,
                    }}
                  />
                  <input
                    type="hidden"
                    name={`newsOrder${i}`}
                    value={article.newsOrder}
                  />

                  <hr class="sliderHR" />
                {/each}
                <input type="hidden" name="length" value={articles.length} />
              </form>
              <button on:click={addArticle}>Add new article</button>
            {/await}
          </div>
        </div>
      {:else if selectedTab == "article order"}
        <div class="settings">
          <div>
            {#await articlesChangeOrder then articles}
              <div class="articles-to-edit-order">
                {#each articles as article, index}
                  <div class="article-order-box">
                    <h3>{article.title}</h3>
                    <div class="article-small-font">{article.text_content}</div>
                    <div class="bottom-arrows">
                      <button
                        on:click={() =>
                          changeArticleOrder("down", index, articles)}
                        ><svg
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 384 512"
                          style="width: 20px; height:20px;"
                          ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                            d="M374.6 246.6C368.4 252.9 360.2 256 352 256s-16.38-3.125-22.62-9.375L224 141.3V448c0 17.69-14.33 31.1-31.1 31.1S160 465.7 160 448V141.3L54.63 246.6c-12.5 12.5-32.75 12.5-45.25 0s-12.5-32.75 0-45.25l160-160c12.5-12.5 32.75-12.5 45.25 0l160 160C387.1 213.9 387.1 234.1 374.6 246.6z"
                          /></svg
                        ></button
                      >
                      <button
                        on:click={() =>
                          changeArticleOrder("up", index, articles)}
                        ><svg
                          xmlns="http://www.w3.org/2000/svg"
                          viewBox="0 0 384 512"
                          style="width: 20px; height:20px;"
                          ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                            d="M374.6 310.6l-160 160C208.4 476.9 200.2 480 192 480s-16.38-3.125-22.62-9.375l-160-160c-12.5-12.5-12.5-32.75 0-45.25s32.75-12.5 45.25 0L160 370.8V64c0-17.69 14.33-31.1 31.1-31.1S224 46.31 224 64v306.8l105.4-105.4c12.5-12.5 32.75-12.5 45.25 0S387.1 298.1 374.6 310.6z"
                          /></svg
                        ></button
                      >
                    </div>
                  </div>
                  {#if index != articles.length - 1}
                    <div class="vertical-line" />
                  {/if}
                {/each}
                <button on:click={() => fetchSaveArticlesOrder()}>Save</button>
              </div>
            {/await}
          </div>
        </div>
      {:else if selectedTab == "footer"}
        <div class="settings">
          <div class="card">
            <form action="/changeCompanyName" method="POST">
              <br />
              <div class="line">
                <h5>Company Name</h5>
                {#await fetchFooterCompanyName then FooterCompanyName}
                  <input
                    type="text"
                    value={FooterCompanyName[0].company}
                    name="companyName"
                  />
                {/await}
              </div>
              <button type="submit">Save</button>
            </form>
            <hr class="sliderHr" />
            {#await fetchFooterItems then footerItems}
              <form action="/uploadFooter" method="POST">
                {#each footerItems as footerItem, i}
                  <div class="card">
                    <div class="line-center">
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 448 512"
                        on:click={() => removeFooterItem(i, footerItems)}
                        style="width: 30px; height:30px;"
                        ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                          d="M135.2 17.69C140.6 6.848 151.7 0 163.8 0H284.2C296.3 0 307.4 6.848 312.8 17.69L320 32H416C433.7 32 448 46.33 448 64C448 81.67 433.7 96 416 96H32C14.33 96 0 81.67 0 64C0 46.33 14.33 32 32 32H128L135.2 17.69zM394.8 466.1C393.2 492.3 372.3 512 346.9 512H101.1C75.75 512 54.77 492.3 53.19 466.1L31.1 128H416L394.8 466.1z"
                        /></svg
                      >
                    </div>
                    <div class="line">
                      <h5>On homepage text content</h5>
                      <input
                        type="text"
                        name={`footerTextContent${i}`}
                        value={footerItem.text_content}
                      />
                    </div>
                    <div class="line">
                      <h5>Content of subpage</h5>
                      <input
                        type="text"
                        name={`footerContent${i}`}
                        value={footerItem.content}
                      />
                    </div>
                    <hr class="sliderHR" />
                  </div>
                {/each}
                <input
                  type="hidden"
                  name="footerLength"
                  value={footerItems.length}
                />
                <button type="submit">Save</button>
              </form>
              <button on:click={() => addFooterItem(footerItems)}
                >Add footer item</button
              >
            {/await}
          </div>
        </div>
      {:else if selectedTab == "ffn"}
        <div class="settings">
          {#await ffn then ffn}
            <form
              action="/uploadFfn"
              enctype="multipart/form-data"
              method="post"
            >
              <div class="line">
                <h5>Title</h5>
                <input type="text" name="title" id="" value={ffn.title} />
              </div>
              <div class="line">
                <h5>Sumamry</h5>
                <input
                  type="text"
                  name="summary"
                  id=""
                  value={ffn.text_content}
                />
              </div>
              <div class="line">
                <h5>Photo (500x500)</h5>
                <input type="file" name="photo" id="" accept="image/*" />
              </div>
              <img
                src={ffn.src}
                style="width: 150px; height: 150px"
                alt=""
              /><br />
              <button type="submit">Save</button>
            </form>
          {/await}
        </div>
      {:else if selectedTab == "users"}
        <div use:getUsers class="card users">
          <div class="editedCard" style="display:none">
            <input type="text" style="display:none" />
          </div>
          {#await usersData then users}
            {#each users as item, i}
              {#if item.admin == 2}
                <div class="userCard" id={"card" + item.rowid}>
                  <img
                    src="./images/admin.png"
                    alt="avatar"
                    width="200px"
                    height="200px"
                  />
                  <h3>{item.username}</h3>
                  <p>email: {item.email}</p>
                  <p>password: {item.password}</p>
                  <h3 style="color:brown; margin:10px;">Administrator</h3>
                  <button
                    on:click={() => {
                      EditUser(
                        item.rowid,
                        item.username,
                        item.email,
                        item.password,
                        item.admin
                      );
                    }}
                    class="buttonUs btnEdit">Edit</button
                  ><br />
                </div>
              {:else if item.admin == 1}
                <div class="userCard" id={"card" + item.rowid}>
                  <img
                    src="./images/avatar.png"
                    alt="avatar"
                    width="150px"
                    height="150px"
                  />
                  <h3>{item.username}</h3>
                  <p>email: {item.email}</p>
                  <p>password: {item.password}</p>
                  <h3 style="color:#00BFFF; margin:10px;">Advanced User</h3>
                  <button
                    on:click={() => {
                      EditUser(
                        item.rowid,
                        item.username,
                        item.email,
                        item.password,
                        item.admin
                      );
                    }}
                    class="buttonUs btnEdit">Edit</button
                  >
                  <br />
                  <button
                    on:click={() => {
                      DeleteUser(item.rowid);
                    }}
                    class="buttonUs btnDelete">Delete</button
                  ><br />
                </div>
              {:else}
                <div class="userCard" id={"card" + item.rowid}>
                  <img
                    src="./images/avatar.png"
                    alt="avatar"
                    width="150px"
                    height="150px"
                  />
                  <h3>{item.username}</h3>
                  <p>email: {item.email}</p>
                  <p>password: {item.password}</p>
                  <h3 style="color:#696969; margin:10px;">Normal user</h3>
                  <button
                    on:click={() => {
                      EditUser(
                        item.rowid,
                        item.username,
                        item.email,
                        item.password,
                        item.admin
                      );
                    }}
                    class="buttonUs btnEdit">Edit</button
                  ><br />
                  <button
                    on:click={() => {
                      DeleteUser(item.rowid);
                    }}
                    class="buttonUs btnDelete">Delete</button
                  >
                </div>
              {/if}
            {/each}
            <div class="editedCard" id="ednormal" style="display:none">
              <img
                src="./images/avatar.png"
                alt="avatar"
                width="130px"
                height="130px"
                id="edImg"
              />
              <label for="username">Username</label>
              <input type="text" name="username" />
              <label for="email">Email</label>
              <input type="text" name="email" />
              <label for="password">Password</label>
              <input type="text" name="password" />
              <label for="permissions">Permission</label>
              <select id="permissions">
                <option value="0">Normal user</option>
                <option value="1">Advanced user</option>
              </select>
              <button class="buttonUs btnEdit" id="saveme">Save</button>
            </div>
            <div id="err" style="display:none;">
              You must fill in all the blanks!
            </div>
            <div class="editedCard" id="edadmin" style="display:none">
              <img
                src="./images/avatar.png"
                alt="avatar"
                width="180px"
                height="180px"
                id="edImg"
              />
              <label for="username">Username</label>
              <input type="text" name="username" />
              <label for="email">Email</label>
              <input type="text" name="email" />
              <label for="password">Password</label>
              <input type="text" name="password" />
              <button class="buttonUs btnEdit" id="saveme">Save</button>
            </div>
            <div id="err" style="display:none;">
              You must fill in all the blanks!
            </div>
          {/await}
        </div>
      {:else if selectedTab == "login to customize"}
        <div class="settings red">LOGIN TO CUSTOMIZE</div>
      {:else if selectedTab == "import_export"}
        <div class="settings">
          <h3>
            In this part of CMS you can generate JSON files, so you can create
            backup of your changes. Default export settings take data from
            template that you created, but if you want to, you can also generate
            backup of data from database
          </h3>
          <hr class="mtb-10" />
          <div class="card">
            <div class="flex center">
              <div class="flex">
                <h3>Database content</h3>
                <label class="switch">
                  <input type="checkbox" id="database_content" />
                  <span class="slider round" />
                </label>
              </div>
            </div>
            <button class="exportButton" on:click={() => exportSettings()}
              ><svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 512 512"
                style="width: 20px; height:20px;"
                ><!--! Font Awesome Pro 6.1.1 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license (Commercial License) Copyright 2022 Fonticons, Inc. --><path
                  d="M480 352h-133.5l-45.25 45.25C289.2 409.3 273.1 416 256 416s-33.16-6.656-45.25-18.75L165.5 352H32c-17.67 0-32 14.33-32 32v96c0 17.67 14.33 32 32 32h448c17.67 0 32-14.33 32-32v-96C512 366.3 497.7 352 480 352zM432 456c-13.2 0-24-10.8-24-24c0-13.2 10.8-24 24-24s24 10.8 24 24C456 445.2 445.2 456 432 456zM233.4 374.6C239.6 380.9 247.8 384 256 384s16.38-3.125 22.62-9.375l128-128c12.49-12.5 12.49-32.75 0-45.25c-12.5-12.5-32.76-12.5-45.25 0L288 274.8V32c0-17.67-14.33-32-32-32C238.3 0 224 14.33 224 32v242.8L150.6 201.4c-12.49-12.5-32.75-12.5-45.25 0c-12.49 12.5-12.49 32.75 0 45.25L233.4 374.6z"
                /></svg
              >Export</button
            >
            <hr class="mtb-10" />
            <h3>Import</h3>
            <input
              type="file"
              accept="application/JSON"
              name=""
              id="importFile"
            />
            <button
              on:click={() =>
                importFromJSON(document.querySelector("#importFile"))}
              >Import</button
            >
          </div>
        </div>
      {/if}
    </div>
  </div>
{/await}
