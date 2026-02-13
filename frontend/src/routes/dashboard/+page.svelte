<script>
  import { onMount } from "svelte";
  import { apiFetch } from "$lib/api";
  import { goto } from "$app/navigation";

  let stats = {
    keyCount: 0,
    documentCount: 0,
    activeKeys: 0,
  };
  let loading = true;

  onMount(async () => {
    try {
      const keys = await apiFetch("/keys");
      stats.keyCount = keys.length;
      stats.documentCount = keys.reduce((sum, k) => sum + k.document_count, 0);
      stats.activeKeys = keys.filter((k) => k.is_active).length;
    } catch (e) {
      console.error("Failed to load stats:", e);
    } finally {
      loading = false;
    }
  });
</script>

<div class="container">
  <div class="header">
    <h1>Dashboard</h1>
    <p class="subtitle">Welcome to your RAG-as-a-Service platform</p>
  </div>

  {#if loading}
    <div class="loading">Loading dashboard...</div>
  {:else}
    <div class="stats">
      <div class="stat-card">
        <div class="stat-number">{stats.keyCount}</div>
        <div class="stat-label">API Keys</div>
        <a href="/api-keys" class="stat-link">Manage Keys</a>
      </div>

      <div class="stat-card">
        <div class="stat-number">{stats.activeKeys}</div>
        <div class="stat-label">Active Keys</div>
        <a href="/api-keys" class="stat-link">View Details</a>
      </div>

      <div class="stat-card">
        <div class="stat-number">{stats.documentCount}</div>
        <div class="stat-label">Documents</div>
        <a href="/ingest" class="stat-link">Upload More</a>
      </div>
    </div>

    <div class="quick-actions">
      <h3>Quick Actions</h3>
      <div class="action-buttons">
        <button class="action-btn" on:click={() => goto("/api-keys")}>
          <span class="btn-title">Create API Key</span>
          <span class="btn-desc">Generate new key for your app</span>
        </button>
        <button class="action-btn" on:click={() => goto("/ingest")}>
          <span class="btn-title">Upload Document</span>
          <span class="btn-desc">Add PDFs to knowledge base</span>
        </button>
        <button class="action-btn" on:click={() => goto("/chat")}>
          <span class="btn-title">Test Chat</span>
          <span class="btn-desc">Try your RAG chatbot</span>
        </button>
        <button class="action-btn" on:click={() => goto("/usage")}>
          <span class="btn-title">View Usage</span>
          <span class="btn-desc">Check your plan limits</span>
        </button>
        <button class="action-btn" on:click={() => goto("/docs")}>
          <span class="btn-title">API Documentation</span>
          <span class="btn-desc">Learn how to integrate</span>
        </button>
      </div>
    </div>
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

  h1 {
    font-size: 2.5rem;
    color: #fff;
    margin-bottom: 10px;
  }

  .subtitle {
    color: #b0b0b0;
    font-size: 1rem;
  }

  .loading {
    text-align: center;
    padding: 60px 20px;
    color: #888;
  }

  .stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 24px;
    margin-bottom: 40px;
  }

  .stat-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0;
    padding: 30px;
    backdrop-filter: blur(10px);
    text-align: center;
  }

  .stat-number {
    font-size: 3rem;
    font-weight: 700;
    color: #64b5f6;
    margin-bottom: 10px;
  }

  .stat-label {
    font-size: 1rem;
    color: #b0b0b0;
    margin-bottom: 16px;
  }

  .stat-link {
    color: #64b5f6;
    text-decoration: none;
    font-size: 0.9rem;
  }

  .quick-actions {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0;
    padding: 30px;
    backdrop-filter: blur(10px);
  }

  .quick-actions h3 {
    color: #fff;
    margin-bottom: 24px;
    text-align: center;
  }

  .action-buttons {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
  }

  .action-btn {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0;
    padding: 20px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    text-align: left;
  }

  .btn-title {
    color: #fff;
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 6px;
    display: block;
  }

  .btn-desc {
    color: #888;
    font-size: 0.85rem;
  }
</style>
