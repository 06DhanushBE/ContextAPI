<script>
  let apiKey = "";
  let file = null;
  let message = "";
  let error = "";
  let loading = false;

  async function upload() {
    error = "";
    message = "";

    if (!apiKey.trim()) {
      error = "Paste your API key";
      return;
    }

    if (!file) {
      error = "Select a PDF file";
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    loading = true;

    try {
      const res = await fetch(
        import.meta.env.VITE_API_BASE + "/ingest",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${apiKey.trim()}`
          },
          body: formData
        }
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      message = `Uploaded ${data.document} (${data.chunks_added} chunks)`;
      file = null;
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  }
</script>

<h1>Upload Knowledge Base</h1>

<label>
  API Key
  <input
    type="password"
    placeholder="sk-xxxxxxxxxxxxxxxx"
    bind:value={apiKey}
  />
</label>

<br /><br />

<input
  type="file"
  accept="application/pdf"
  on:change={(e) => (file = e.target.files[0])}
/>

<br /><br />

<button on:click={upload} disabled={loading}>
  {loading ? "Uploading..." : "Upload"}
</button>

{#if message}
  <p style="color: green">{message}</p>
{/if}

{#if error}
  <p style="color: red">{error}</p>
{/if}
