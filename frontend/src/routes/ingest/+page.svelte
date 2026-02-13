<script>
  import { goto } from "$app/navigation";

  let apiKey = "";
  let file = null;
  let fileName = "";
  let message = "";
  let error = "";
  let loading = false;

  async function upload() {
    error = "";
    message = "";

    if (!apiKey.trim()) {
      error = "Please paste your API key";
      return;
    }

    if (!file) {
      error = "Please select a PDF file";
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    loading = true;

    try {
      const res = await fetch(import.meta.env.VITE_API_BASE + "/ingest", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${apiKey.trim()}`,
        },
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Upload failed");
      }

      message = `Uploaded "${data.document}" - ${data.chunks_added} chunks added`;
      file = null;
      fileName = "";

      // Redirect to chat after 2 seconds
      setTimeout(() => {
        goto("/chat");
      }, 2000);
    } catch (e) {
      error = e?.message || "Upload failed";
    } finally {
      loading = false;
    }
  }

  function handleFileChange(e) {
    const target = /** @type {HTMLInputElement} */ (e.target);
    file = target.files?.[0] || null;
    fileName = file ? file.name : "";
  }

  function clearFile() {
    file = null;
    fileName = "";
  }
</script>

<div class="container">
  <div class="header">
    <h1>Upload Knowledge Base</h1>
    <p class="subtitle">
      Upload PDF documents to create your custom RAG knowledge base
    </p>
  </div>

  <div class="nav-link">
    <a href="/api-keys">Back to API Keys</a>
  </div>

  <div class="upload-card">
    <div class="form-group">
      <label for="api-key">
        <span class="label-text">API Key</span>
        <span class="label-hint">(Get this from the API Keys page)</span>
      </label>
      <input
        id="api-key"
        type="password"
        placeholder="sk-xxxxxxxxxxxxxxxx"
        bind:value={apiKey}
        class="input-field"
      />
    </div>

    <div class="form-group">
      <label for="file-upload" class="label-text">Select PDF File</label>
      <div class="file-input-wrapper">
        <input
          id="file-upload"
          type="file"
          accept="application/pdf"
          on:change={handleFileChange}
          class="file-input"
        />
        {#if fileName}
          <div class="file-selected">
            <span class="file-name">{fileName}</span>
            <button type="button" on:click={clearFile} class="clear-btn"
              >✕</button
            >
          </div>
        {:else}
          <div class="file-placeholder">
            <span>Click to select PDF or drag & drop</span>
          </div>
        {/if}
      </div>
    </div>

    <button
      on:click={upload}
      disabled={loading || !apiKey.trim() || !file}
      class="upload-btn"
      class:loading
    >
      {#if loading}
        <span class="spinner"></span> Uploading...
      {:else}
        Upload & Process
      {/if}
    </button>

    {#if message}
      <div class="message success">{message}</div>
    {/if}

    {#if error}
      <div class="message error">{error}</div>
    {/if}
  </div>

  <div class="info-section">
    <h3>How it works</h3>
    <ol>
      <li>
        Paste your API key (create one in <a href="/api-keys">API Keys</a>)
      </li>
      <li>Select a PDF document from your computer</li>
      <li>Click "Upload & Process" - we'll chunk and embed it</li>
      <li>
        Start chatting with your documents in the <a href="/chat">Chat</a> page
      </li>
    </ol>
  </div>
</div>

<style>
  .container {
    max-width: 700px;
    margin: 40px auto;
    padding: 0 20px;
  }

  .header {
    text-align: center;
    margin-bottom: 30px;
  }

  h1 {
    font-size: 2rem;
    margin-bottom: 10px;
    color: #fff;
  }

  .subtitle {
    color: #b0b0b0;
    font-size: 0.95rem;
  }

  .nav-link {
    margin-bottom: 20px;
  }

  .nav-link a {
    color: #0066cc;
    text-decoration: none;
    font-size: 0.9rem;
  }

  .upload-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0;
    padding: 30px;
    backdrop-filter: blur(10px);
    margin-bottom: 30px;
  }

  .form-group {
    margin-bottom: 24px;
  }

  label {
    display: block;
    margin-bottom: 8px;
  }

  .label-text {
    font-weight: 600;
    color: #fff;
    font-size: 0.95rem;
  }

  .label-hint {
    color: #888;
    font-size: 0.85rem;
    margin-left: 8px;
  }

  .input-field {
    width: 100%;
    padding: 12px 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 0;
    font-size: 1rem;
    color: #fff;
    transition: all 0.2s;
  }

  .input-field:focus {
    outline: none;
    border-color: #64b5f6;
    background: rgba(255, 255, 255, 0.08);
  }

  .file-input-wrapper {
    position: relative;
  }

  .file-input {
    position: absolute;
    opacity: 0;
    width: 100%;
    height: 100%;
    cursor: pointer;
  }

  .file-placeholder,
  .file-selected {
    padding: 20px;
    border: 2px dashed rgba(255, 255, 255, 0.3);
    border-radius: 0;
    text-align: center;
    background: rgba(255, 255, 255, 0.02);
  }

  .file-selected {
    border-style: solid;
    border-color: #4caf50;
    background: rgba(76, 175, 80, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .file-name {
    font-weight: 500;
    color: #fff;
  }

  .clear-btn {
    background: #ff4444;
    color: white;
    border: none;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    cursor: pointer;
    font-size: 0.9rem;
  }

  .upload-btn {
    width: 100%;
    padding: 14px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 0;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
  }

  .upload-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .upload-btn.loading {
    opacity: 0.8;
  }

  .spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .message {
    margin-top: 20px;
    padding: 12px 16px;
    border-radius: 0;
    font-size: 0.95rem;
  }

  .message.success {
    background: rgba(76, 175, 80, 0.2);
    color: #4caf50;
    border: 1px solid rgba(76, 175, 80, 0.3);
  }

  .message.error {
    background: rgba(244, 67, 54, 0.2);
    color: #ff5252;
    border: 1px solid rgba(244, 67, 54, 0.3);
  }

  .info-section {
    background: rgba(100, 181, 246, 0.1);
    padding: 24px;
    border-radius: 12px;
    border-left: 4px solid #64b5f6;
  }

  .info-section h3 {
    margin-top: 0;
    margin-bottom: 16px;
    color: #64b5f6;
  }

  .info-section ol {
    margin: 0;
    padding-left: 20px;
  }

  .info-section li {
    margin-bottom: 8px;
    color: #b0b0b0;
    line-height: 1.6;
  }
</style>
