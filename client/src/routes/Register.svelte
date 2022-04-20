<script>
  async function submit(){
    let login = document.getElementsByName("username")[0].value
    let pass = document.getElementsByName("password")[0].value
    let passconfirm = document.getElementsByName("password2")[0].value
    let email = document.getElementsByName("email")[0].value
    if([login,pass,passconfirm,email].includes("")) emptyInputError()
    else if(pass != passconfirm) passwordConfirmError()
    else{
      document.querySelector("#errordisplay").style.display = "none"
      const body = JSON.stringify({ username:login, password:pass, email:email })
      const headers = { "Content-Type": "application/json" }
      fetch("/register", { method: "post", body, headers })
        .then(response => response.json())
        .then(
          data => {
              console.log(data)
              if(!data.correctData) userAlreadyExistsError()
              else window.location.replace("/#/login")
        }
        )
        
    }
  } 
  async function passwordConfirmError(){
    document.querySelector("#errordisplay").textContent = "Passwords are not identical!"
    document.querySelector("#errordisplay").style.display = "block"
    document.getElementsByName("password")[0].value = ""
    document.getElementsByName("password2")[0].value = ""
  }
  async function emptyInputError(){
    document.querySelector("#errordisplay").textContent = "You must fill in all the blanks!"
    document.querySelector("#errordisplay").style.display = "block"
  }
  async function userAlreadyExistsError(){
      document.querySelector("#errordisplay").textContent = "User with that username already exists!"
      document.querySelector("#errordisplay").style.display = "block"
   }
</script>


<div class="all">
  <div class="login-box">
    <h1>Sign up</h1>
    <input type="text" name="username" placeholder="Username" />
    <input type="text" name="email" placeholder="E-mail" />
    <input type="password" name="password" placeholder="Password" />
    <input type="password" name="password2" placeholder="Retype password" />
    <input type="submit" id="submitbutton" name="signup_submit" value="Sign me up" on:click={submit}/>
    <a href="/#/login" class="switchlogin">I already have an account</a>
</div>
<div class="errorloginregister" id="errordisplay">
</div>
</div>


<style>
  :global(body) {
    margin: 0;
    padding: 0;
    /* background: #ddd; */
    /*overflow:hidden;*/
  }
</style>
