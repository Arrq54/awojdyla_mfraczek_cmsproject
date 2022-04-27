<script>
  import Router from "svelte-spa-router";

  import Register from "./routes/Register.svelte";
  import Login from "./routes/Login.svelte";
  import HomePageCms from "./routes/HomePageCms.svelte";
  import ConfigurationMenuUser from "./routes/ConfigurationMenuUser.svelte";
  import Article from "./routes/Article.svelte";

  export let name;
</script>

<main>
  <Router
    routes={{
      "/": HomePageCms,
      "/register": Register,
      "/login": Login,
      "/configurationUser": ConfigurationMenuUser,
      "/article/:id": Article,
    }}
  />
</main>
