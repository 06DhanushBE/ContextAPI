<script>
  import { apiFetch } from "$lib/api";
  let keys = [];

  async function load() {
    keys = await apiFetch("/keys");
  }

  async function createKey() {
    const res = await apiFetch("/keys", { method: "POST" });

    // Save locally (browser only)
    const stored = JSON.parse(localStorage.getItem("api_keys") || "{}");
    stored[res.id] = res.api_key;
    localStorage.setItem("api_keys", JSON.stringify(stored));

    alert("SAVE THIS KEY:\n" + res.api_key);
    load();
  }


  async function revoke(id) {
    await apiFetch(`/keys/${id}`, { method: "DELETE" });
    load();
  }

  load();
</script>

<h1>API Keys</h1>

<button on:click={createKey}>Create Key</button>

<ul>
  {#each keys as k}
    <li>
      Key #{k.id} — {k.is_active ? "Active" : "Revoked"}
      {#if k.is_active}
        <button on:click={() => revoke(k.id)}>Revoke</button>
      {/if}
    </li>
  {/each}
</ul>
