<script>
  window.onload = () => {
    const body = JSON.stringify({});
    const headers = { "Content-Type": "application/json" };
    fetch("/checkLoginStatus", { method: "post", body, headers })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        //   if(data.user == 0 || data.user == 2) window.location.replace("/")
        //   else if(data.user == 1) standardUser()
      });
  };
</script>

<div id="backg" />
<div class="maincontainer">
  <div class="menu">
    <div class="maincard">
      <ul>
        <li>Themes</li>
        <li>Slider</li>
        <li>Menu</li>
        <li>Articles</li>
        <li>Pictures</li>
      </ul>
    </div>
    <p>No admin permissions</p>
  </div>
</div>

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
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-family: "Roboto", sans-serif;
    background: whitesmoke;
    border: 1px solid whitesmoke;
    border-radius: 26px;
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
</style>
