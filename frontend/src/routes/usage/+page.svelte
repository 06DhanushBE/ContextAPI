<script>
  import { apiFetch } from "$lib/api";
  let data;

  async function load() {
    data = await apiFetch("/usage");
  }

  load();
</script>

<h1>Usage</h1>

{#if data}
  <p>Plan: {data.plan}</p>

  <h3>Ingestion</h3>
  <p>{data.usage.ingested_chars} / {data.limits.max_ingested_chars}</p>

  <h3>Chat Tokens</h3>
  <p>{data.usage.chat_tokens} / {data.limits.max_chat_tokens}</p>
{/if}
