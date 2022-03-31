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
      "/register": Register,
      "/login": Login,
      "/Home": HomePageCms,
    }}
  />
</main>
