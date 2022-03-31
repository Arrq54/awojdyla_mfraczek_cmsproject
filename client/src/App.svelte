<script>
  import Router from "svelte-spa-router";

  import Register from "./routes/Register.svelte";
  import Login from "./routes/Login.svelte";
  import HomePageCms from "./routes/HomePageCms.svelte";

  export let name;
</script>

<main>
  <Router
    routes={{
      "/": HomePageCms,
      "/register": Register,
      "/login": Login,
    }}
  />
</main>
