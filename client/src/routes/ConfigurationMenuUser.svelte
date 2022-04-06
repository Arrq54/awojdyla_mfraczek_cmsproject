<script defer>
  window.onload = function(){
    console.log("asd")

    // fetch("/checkLoginStatus")
    //   .then((response) => response.json())
    //   .then((data) => {
    //     console.log(data);
    //     //   if(data.user == 0 || data.user == 2) window.location.replace("/")
    //     //   else if(data.user == 1) standardUser()
    //   });
  }
  async function asyncCheckLoginStatus(){
    let temp = fetch("/checkLoginStatus").then((response) => response.json())
    return await temp
  }
  $: status = asyncCheckLoginStatus()
  $: selectedTab = 'themes'
  function setTab(tab){
    selectedTab = tab
  }
  function sliderLoaded(){
    console.log("slider loaded")
  }
</script>
<div id="backg" />
<!-- svelte-ignore missing-declaration -->
{#await status then user}
<div class="maincontainer">
  <div class="menu">
    <div class="maincard">
      <ul>
        <li  on:click={()=>setTab('themes')}>Themes</li>
        <li on:click={()=>setTab('slider')}>Slider</li>
        <li on:click={()=>setTab('menu')}>Menu</li>
        <li on:click={()=>setTab('articles')}>Articles</li>
        <li on:click={()=>setTab('pictures')}>Pictures</li>
      </ul>
    </div>
    {#if user.user==2}
    <p>Admin</p>
    {:else}
    <p>No admin permissions</p>
    {/if}
  </div>
  <div class="content">
    {#if selectedTab=='themes'}
    <!-- THEMES EDYCJA -->
      <div class="settings flex">
        <div class="line">
          Themes
        </div>
      </div>
      {:else if selectedTab=='slider'}
      <div  on:load={()=>sliderLoaded()} class="settings flex">
        <!-- SLIDER EDYCJA -->
        <div class="card">
          <div class="line">
            <h5>Tu bedzie opis</h5>
            <input type="text" name="" id="">
          </div>
          <div class="line">
            <h5>Tu bedzie nizej opis</h5>
            <input type="text" name="" id="">
          </div>
        </div>
      </div>
      {:else if selectedTab=="menu"}
      <div>
        <!-- MENU EDYCJA -->
        menu
      </div>
      {:else if selectedTab=="articles"}
      <!-- ARTICLES EDYCJA -->
      <div>
        articles
      </div>
      {:else if selectedTab=="pictures"}
      <!-- Pictures EDYCJA -->
      <div>
        pictures
      </div>
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
    height: 500px;
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
    height: 100%;
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
  .content{
    width: 88%;
    height: 100%;
    padding: 0px;
  }
  .flex{
    display: flex;
  }
  .line{
    display: flex;
    justify-content: space-between;
  }
</style>
