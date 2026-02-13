<script>
  import { onMount } from "svelte";
  import { apiFetch } from "$lib/api";
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";

  let apiKeyId = null;
  let documents = [];
  let loading = true;
  let error = "";
  let deleting = null;

  onMount(async () => {
    apiKeyId = $page.url.searchParams.get("key_id");
    if (!apiKeyId || apiKeyId === "undefined") {
      console.error("No valid key_id in URL:", apiKeyId);
      goto("/api-keys");
      return;
    }
    await loadDocuments();
  });

  async function loadDocuments() {
    loading = true;
    error = "";
    try {
      documents = await apiFetch(`/documents/api-key/${apiKeyId}`);
    } catch (e) {
      error = e?.message || "Failed to load documents";
    } finally {
      loading = false;
    }
  }

  async function deleteDocument(docId, filename) {
    if (!confirm(`Delete "${filename}"? This will remove all vectors.`)) {
      return;
    }

    deleting = docId;
    try {
      await apiFetch(`/documents/${docId}`, { method: "DELETE" });
      documents = documents.filter((d) => d.id !== docId);
    } catch (e) {
      error = e?.message || "Failed to delete document";
    } finally {
      deleting = null;
    }
  }

  function formatDate(dateStr) {
    return new Date(dateStr).toLocaleString();
  }

  function formatSize(chars) {
    if (chars < 1000) return `${chars} chars`;
    return `${(chars / 1000).toFixed(1)}K chars`;
  }
</script>

<h1>Documents for API Key #{apiKeyId}</h1>

<p>
  <a href="/api-keys">← Back to API Keys</a>
  |
  <a
    href="/ingest"
    on:click={(e) => {
      e.preventDefault();
      const stored = JSON.parse(localStorage.getItem("api_keys") || "{}");
      const apiKey = stored[apiKeyId];
      if (apiKey) {
        localStorage.setItem("active_api_key_id", apiKeyId);
        localStorage.setItem("active_api_key", apiKey);
        window.location.href = "/ingest";
      } else {
        alert("API key not found. You need to save it when created.");
      }
    }}>Upload Document</a
  >
</p>

{#if loading}
  <p>Loading documents...</p>
{:else if error}
  <p style="color: red">{error}</p>
{:else if documents.length === 0}
  <p>
    No documents uploaded yet. <a href="/ingest">Upload your first document</a>
  </p>
{:else}
  <table>
    <thead>
      <tr>
        <th>Filename</th>
        <th>Size</th>
        <th>Chunks</th>
        <th>Uploaded</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      {#each documents as doc}
        <tr>
          <td>{doc.filename}</td>
          <td>{formatSize(doc.char_count)}</td>
          <td>{doc.chunk_count}</td>
          <td>{formatDate(doc.created_at)}</td>
          <td>
            <button
              on:click={() => deleteDocument(doc.id, doc.filename)}
              disabled={deleting === doc.id}
              style="background: #dc3545; color: white"
            >
              {deleting === doc.id ? "Deleting..." : "Delete"}
            </button>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
{/if}

<style>
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }

  th,
  td {
    padding: 12px;
    text-align: left;
    border-bottom: 1px solid #ddd;
  }

  th {
    background-color: #f5f5f5;
    font-weight: bold;
  }

  button {
    padding: 6px 12px;
    border: none;
    border-radius: 0;
    cursor: pointer;
  }

  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
</style>
