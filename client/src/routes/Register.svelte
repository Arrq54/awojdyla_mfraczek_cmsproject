<script>
  window.onload = function () {
    fetch("test")
      .then((response) => response.json())
      .then((data) => console.log(data));
  };
</script>
<svelte:head><link rel="stylesheet" href="/loginregister.css"></svelte:head>
  <div class="login-box">
      <h1>Sign up</h1>
      <input type="text" name="username" placeholder="Username" />
      <input type="text" name="email" placeholder="E-mail" />
      <input type="password" name="password" placeholder="Password" />
      <input type="password" name="password2" placeholder="Retype password" />
      <input type="submit" id="submitbutton" name="signup_submit" value="Sign me up" />
      <a href="/#/login" class="switchlogin">I already have an account</a>
  </div>

<style>
    :global(body) {
    margin: 0;
    padding: 0;
    background: #ddd;
  }
</style>