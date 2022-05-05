<script>
  import { Router, Link } from "svelte-navigator";
  export let params = {};
  let fecthMenu = getArticle(params.id);
  async function getArticle(id) {
    const body = JSON.stringify({ body: parseInt(id) });
    console.log(body);
    const headers = { "Content-Type": "application/json" };
    let response = await fetch("/getFooterItemById", {
      method: "post",
      body,
      headers,
    }).then((response) => response.json());
    return response[0];
  }
  console.log(params.id);
</script>

{#await fecthMenu then item}
  <h1>{item.text_content}</h1>
  <div class="menu-content">{item.content}</div>
{/await}

<style>
  .menu-content {
    white-space: pre-wrap;
  }
</style>
