<script>
  async function submit(){
    let login = document.getElementsByName("username")[0].value
    let pass = document.getElementsByName("password")[0].value
    if([login,pass].includes("")) emptyInputError()
    else{
      document.querySelector("#errordisplay").style.display = "none"
       const body = JSON.stringify({ username:login, password:pass })
       const headers = { "Content-Type": "application/json" }
       fetch("/attemptLogin", { method: "post", body, headers })
        .then(response => response.json())
        .then(
            data => {
              console.log(data)
              if(!data.correctData) userNotFound()
              else {
                localStorage.setItem('user', login)
                window.location.replace("/")
              }
            }
        )
    }
  } 
  async function emptyInputError(){ 
      document.querySelector("#errordisplay").textContent = "You must fill in all the blanks!"
      document.querySelector("#errordisplay").style.display = "block"
   }
   async function userNotFound(){ 
      document.querySelector("#errordisplay").textContent = "User with that data not found!"
      document.querySelector("#errordisplay").style.display = "block"
   }
</script>
<div class="all"> 
  <div class="login-box" style="height:310px">
    <h1>Log in</h1>
    <input type="text" name="username" placeholder="Username" />
    <input type="password" name="password" placeholder="Password" />
    <input type="submit" id="submitbutton" name="signup_submit" value="Log me in" on:click={submit}/>
    <a href="/#/register" class="switchlogin">Create an account</a>
  </div>
  <div class="errorloginregister" id="errordisplay">
  </div>
</div>
