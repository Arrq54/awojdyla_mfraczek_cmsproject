<script>
  import Router from "svelte-spa-router";

  import HomePageCms from "./routes/HomePageCms.svelte";

  export let name;
</script>

<main>
  <Router
    routes={{
      "/Home": HomePageCms,
    }}
  />
</main>

