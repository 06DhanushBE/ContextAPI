<script>
  import { apiFetch } from "$lib/api";
  import { goto } from "$app/navigation";
  import ApiKeyModal from "$lib/ApiKeyModal.svelte";

  let keys = [];
  let loading = false;
  let deleting = null;
  let selectedLlm = "groq";
  let showModal = false;
  let modalData = { apiKey: "", llmProvider: "", keyId: null };

  async function load() {
    loading = true;
    try {
      keys = await apiFetch("/keys");
    } finally {
      loading = false;
    }
  }

  async function createKey() {
    const res = await apiFetch("/keys", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ llm_provider: selectedLlm }),
    });

    // Show modal
    modalData = {
      apiKey: res.api_key,
      llmProvider: res.llm_provider,
      keyId: res.id,
    };
    showModal = true;

    load();
  }

  async function deleteKey(id) {
    if (
      !confirm(
        "PERMANENTLY DELETE this API key and ALL its documents?\nThis cannot be undone!",
      )
    ) {
      return;
    }

    deleting = id;
    try {
      const res = await apiFetch(`/keys/${id}`, { method: "DELETE" });
      alert(`Deleted! ${res.documents_deleted} documents removed.`);
      load();
    } catch (e) {
      alert("Failed to delete: " + (e?.message || "Unknown error"));
    } finally {
      deleting = null;
    }
  }

  function viewDocuments(keyId) {
    goto(`/documents?key_id=${keyId}`);
  }

  async function toggleKey(keyId) {
    try {
      const res = await apiFetch(`/keys/${keyId}/toggle`, { method: "POST" });
      alert(res.message);
      load();
    } catch (e) {
      alert("Failed to toggle: " + (e?.message || "Unknown error"));
    }
  }

  load();
</script>

<ApiKeyModal
  bind:show={showModal}
  apiKey={modalData.apiKey}
  llmProvider={modalData.llmProvider}
  keyId={modalData.keyId}
/>

<div class="container">
  <div class="header">
    <h1>API Keys</h1>
    <p class="subtitle">Manage your API keys and LLM provider settings</p>
  </div>

  <div class="create-section">
    <div class="llm-selector">
      <label for="llm-select">LLM Provider:</label>
      <select id="llm-select" bind:value={selectedLlm}>
        <option value="groq">Groq (Fast & Free)</option>
        <option value="openai">OpenAI (GPT Models)</option>
      </select>
    </div>
    <button on:click={createKey} class="create-btn">Create New API Key</button>
  </div>

  <br /><br />

  {#if loading}
    <p>Loading keys...</p>
  {:else if keys.length === 0}
    <p>No API keys yet. Create one to get started!</p>
  {:else}
    <table>
      <thead>
        <tr>
          <th>Key ID</th>
          <th>Status</th>
          <th>LLM</th>
          <th>Documents</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {#each keys as k}
          <tr>
            <td>#{k.id}</td>
            <td>
              <span style="color: {k.is_active ? 'green' : 'red'}">
                {k.is_active ? "Active" : "Inactive"}
              </span>
            </td>
            <td>
              <span class="llm-badge llm-{k.llm_provider}">
                {k.llm_provider}
              </span>
            </td>
            <td>{k.document_count}</td>
            <td>
              <button
                on:click={() => toggleKey(k.id)}
                style="background: {k.is_active ? '#ffc107' : '#28a745'}"
              >
                {k.is_active ? "Deactivate" : "Activate"}
              </button>
              <button on:click={() => viewDocuments(k.id)}>
                Manage Documents
              </button>
              <button
                on:click={() => deleteKey(k.id)}
                disabled={deleting === k.id}
                style="background: #dc3545; color: white; margin-left: 8px"
              >
                {deleting === k.id ? "Deleting..." : "Delete Permanently"}
              </button>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
</div>

<style>
  .container {
    max-width: 1200px;
    margin: 40px auto;
    padding: 0 20px;
  }

  .header {
    text-align: center;
    margin-bottom: 40px;
  }

  .subtitle {
    color: #b0b0b0;
    font-size: 1rem;
    margin-top: 10px;
  }

  h1 {
    margin-bottom: 1.5rem;
    color: #fff;
    text-align: center;
  }

  .create-section {
    display: flex;
    gap: 1rem;
    align-items: center;
    justify-content: center;
    margin-bottom: 2rem;
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0;
    backdrop-filter: blur(10px);
    flex-wrap: wrap;
  }

  .llm-selector {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .llm-selector label {
    font-weight: 600;
    color: #fff;
  }

  .llm-selector select {
    padding: 0.5rem 1rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 0;
    color: #fff;
    cursor: pointer;
    font-size: 0.95rem;
  }

  .create-btn {
    padding: 0.75rem 1.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 0;
    font-weight: 600;
    cursor: pointer;
  }

  .llm-badge {
    padding: 0.25rem 0.75rem;
    border-radius: 0;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
  }

  .llm-groq {
    background: rgba(76, 175, 80, 0.2);
    color: #4caf50;
    border: 1px solid rgba(76, 175, 80, 0.3);
  }

  .llm-openai {
    background: rgba(33, 150, 243, 0.2);
    color: #64b5f6;
    border: 1px solid rgba(33, 150, 243, 0.3);
  }

  button {
    padding: 8px 16px;
    margin: 4px;
    border: none;
    border-radius: 0;
    background: #667eea;
    color: white;
    cursor: pointer;
  }

  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 0;
    overflow: hidden;
  }

  th,
  td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  th {
    background: rgba(255, 255, 255, 0.08);
    font-weight: 600;
    color: #fff;
  }

  td {
    color: #e0e0e0;
  }

  p {
    color: #b0b0b0;
    text-align: center;
    padding: 40px 20px;
  }
</style>
