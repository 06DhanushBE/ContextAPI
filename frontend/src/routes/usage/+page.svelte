<script>
  import { apiFetch } from "$lib/api";
  import { onMount } from "svelte";

  let data = null;
  let loading = true;
  let error = "";

  onMount(async () => {
    try {
      data = await apiFetch("/usage");
    } catch (e) {
      error = e?.message || "Failed to load usage data";
    } finally {
      loading = false;
    }
  });

  function getPercentage(used, limit) {
    if (!limit) return 0;
    return Math.min(100, (used / limit) * 100);
  }

  function formatNumber(num) {
    if (!num) return "0";
    return num.toLocaleString();
  }
</script>

<div class="container">
  <div class="header">
    <h1>Usage & Limits</h1>
    <p class="subtitle">Track your resource consumption and plan limits</p>
  </div>

  {#if loading}
    <div class="loading">Loading usage data...</div>
  {:else if error}
    <div class="error-message">{error}</div>
  {:else if data}
    <div class="plan-card">
      <h2>Current Plan</h2>
      <div class="plan-name">{data.plan}</div>
    </div>

    <div class="usage-grid">
      <div class="usage-card">
        <h3>Ingested Characters</h3>
        <div class="usage-stats">
          <div class="usage-numbers">
            <span class="current"
              >{formatNumber(data.usage.ingested_chars)}</span
            >
            <span class="separator">/</span>
            <span class="limit"
              >{formatNumber(data.limits.max_ingested_chars)}</span
            >
          </div>
          <div class="usage-bar">
            <div
              class="usage-fill"
              style="width: {getPercentage(
                data.usage.ingested_chars,
                data.limits.max_ingested_chars,
              )}%"
            ></div>
          </div>
          <div class="usage-percent">
            {getPercentage(
              data.usage.ingested_chars,
              data.limits.max_ingested_chars,
            ).toFixed(1)}% used
          </div>
        </div>
      </div>

      <div class="usage-card">
        <h3>Chat Tokens</h3>
        <div class="usage-stats">
          <div class="usage-numbers">
            <span class="current">{formatNumber(data.usage.chat_tokens)}</span>
            <span class="separator">/</span>
            <span class="limit"
              >{formatNumber(data.limits.max_chat_tokens)}</span
            >
          </div>
          <div class="usage-bar">
            <div
              class="usage-fill"
              style="width: {getPercentage(
                data.usage.chat_tokens,
                data.limits.max_chat_tokens,
              )}%"
            ></div>
          </div>
          <div class="usage-percent">
            {getPercentage(
              data.usage.chat_tokens,
              data.limits.max_chat_tokens,
            ).toFixed(1)}% used
          </div>
        </div>
      </div>
    </div>

    <div class="info-card">
      <h3>About Usage Limits</h3>
      <ul>
        <li>
          <strong>Ingested Characters:</strong> Total characters from all uploaded
          PDFs this month
        </li>
        <li>
          <strong>Chat Tokens:</strong> Total tokens used in chat responses this
          month
        </li>
        <li>
          <strong>Resets:</strong> Usage counters reset at the beginning of each
          month
        </li>
      </ul>
    </div>
  {/if}
</div>

<style>
  .container {
    max-width: 900px;
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

  .loading,
  .error-message {
    text-align: center;
    padding: 60px 20px;
    color: #888;
  }

  .error-message {
    color: #ff5252;
  }

  .plan-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0;
    padding: 30px;
    backdrop-filter: blur(10px);
    text-align: center;
    margin-bottom: 30px;
  }

  .plan-card h2 {
    color: #b0b0b0;
    font-size: 0.9rem;
    font-weight: 600;
    text-transform: uppercase;
    margin-bottom: 10px;
  }

  .plan-name {
    font-size: 2rem;
    color: #64b5f6;
    font-weight: 700;
    text-transform: capitalize;
  }

  .usage-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 24px;
    margin-bottom: 30px;
  }

  .usage-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0;
    padding: 24px;
    backdrop-filter: blur(10px);
  }

  .usage-card h3 {
    color: #fff;
    font-size: 1.1rem;
    margin-bottom: 20px;
  }

  .usage-numbers {
    display: flex;
    align-items: baseline;
    gap: 8px;
    margin-bottom: 16px;
  }

  .current {
    font-size: 2rem;
    font-weight: 700;
    color: #64b5f6;
  }

  .separator {
    color: #666;
    font-size: 1.5rem;
  }

  .limit {
    font-size: 1.2rem;
    color: #888;
  }

  .usage-bar {
    height: 8px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 0;
    overflow: hidden;
    margin-bottom: 10px;
  }

  .usage-fill {
    height: 100%;
    background: linear-gradient(90deg, #64b5f6 0%, #667eea 100%);
    transition: width 0.3s ease;
  }

  .usage-percent {
    color: #b0b0b0;
    font-size: 0.85rem;
  }

  .info-card {
    background: rgba(100, 181, 246, 0.1);
    border: 1px solid rgba(100, 181, 246, 0.2);
    border-radius: 0;
    padding: 24px;
  }

  .info-card h3 {
    color: #64b5f6;
    font-size: 1.1rem;
    margin-bottom: 16px;
  }

  .info-card ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .info-card li {
    color: #b0b0b0;
    margin-bottom: 12px;
    padding-left: 20px;
    position: relative;
  }

  .info-card li::before {
    content: "•";
    color: #64b5f6;
    position: absolute;
    left: 0;
  }

  .info-card strong {
    color: #fff;
  }
</style>
