<script>
  window.onload = function () {
    fetch("test")
      .then((response) => response.json())
      .then((data) => console.log(data));
  };
</script>
<svelte:head><link rel="stylesheet" href="/loginregister.css"></svelte:head>
  <div class="login-box" style="height:310px">
      <h1>Log in</h1>
      <input type="text" name="username" placeholder="Username" />
      <input type="password" name="password" placeholder="Password" />
      <input type="submit" id="submitbutton" name="signup_submit" value="Log me in" />
      <a href="/#/register" class="switchlogin">Create an account</a>
  </div>