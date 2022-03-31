<script>
  import Router from "svelte-spa-router";

  import Home from "./routes/Home.svelte";
  import Register from "./routes/Register.svelte"
  import Login from "./routes/Login.svelte"

  export let name;
</script>

<main>
  <Router
    routes={{
      "/": Home,
      "/register": Register,
      "/login": Login,
    }}
  />
</main>

<style>
  main {
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
  }

  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4em;
    font-weight: 100;
  }

  @media (min-width: 640px) {
    main {
      max-width: none;
    }
  }
</style>
