<script>
  let query = "";
  let answer = "";
  let apiKey = "";
  let error = "";
  let loading = false;
  let conversationHistory = [];

  async function ask() {
    if (!apiKey.trim()) {
      error = "Please paste your API key";
      return;
    }

    if (!query.trim()) {
      error = "Please enter a question";
      return;
    }

    error = "";
    loading = true;

    // Add user question to history
    conversationHistory = [
      ...conversationHistory,
      { role: "user", content: query },
    ];
    const currentQuery = query;
    query = ""; // Clear input

    try {
      const res = await fetch(import.meta.env.VITE_API_BASE + "/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${apiKey.trim()}`,
        },
        body: JSON.stringify({ query: currentQuery }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Request failed");
      }

      // Add AI answer to history
      conversationHistory = [
        ...conversationHistory,
        { role: "assistant", content: data.answer },
      ];
    } catch (e) {
      error = e?.message || "An error occurred";
      // Remove the user question if request failed
      conversationHistory = conversationHistory.slice(0, -1);
      query = currentQuery; // Restore the query
    } finally {
      loading = false;
    }
  }

  function handleKeyPress(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      ask();
    }
  }

  function clearChat() {
    conversationHistory = [];
    answer = "";
    error = "";
  }
</script>

<div class="container">
  <div class="header">
    <h1>Chat with Your Documents</h1>
    <p class="subtitle">
      Ask questions and get AI-powered answers from your knowledge base
    </p>
  </div>

  <div class="nav-links">
    <a href="/api-keys">API Keys</a>
    <a href="/ingest">Upload Documents</a>
  </div>

  <div class="chat-card">
    <div class="api-key-section">
      <label for="api-key">
        <span class="label-text">API Key</span>
      </label>
      <input
        id="api-key"
        type="password"
        placeholder="sk-xxxxxxxxxxxxxxxx"
        bind:value={apiKey}
        class="input-field"
      />
    </div>

    <div class="conversation-container">
      {#if conversationHistory.length === 0}
        <div class="empty-state">
          <p>No messages yet. Start by asking a question!</p>
        </div>
      {:else}
        <div class="messages">
          {#each conversationHistory as message}
            <div class="message {message.role}">
              <div class="message-avatar">
                {message.role === "user" ? "USER" : "AI"}
              </div>
              <div class="message-content">
                {message.content}
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>

    {#if error}
      <div class="error-message">{error}</div>
    {/if}

    <div class="input-section">
      <textarea
        placeholder="Ask a question... (Press Enter to send, Shift+Enter for new line)"
        bind:value={query}
        on:keypress={handleKeyPress}
        class="query-input"
        rows="3"
        disabled={loading}
      ></textarea>
      <div class="button-group">
        <button
          on:click={ask}
          disabled={loading || !apiKey.trim() || !query.trim()}
          class="ask-btn"
        >
          {#if loading}
            <span class="spinner"></span> Thinking...
          {:else}
            Ask
          {/if}
        </button>
        {#if conversationHistory.length > 0}
          <button on:click={clearChat} class="clear-btn" disabled={loading}>
            Clear Chat
          </button>
        {/if}
      </div>
    </div>
  </div>
</div>

<style>
  .container {
    max-width: 900px;
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

  .nav-links {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
  }

  .nav-links a {
    color: #0066cc;
    text-decoration: none;
    font-size: 0.9rem;
  }

  .chat-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0;
    padding: 30px;
    backdrop-filter: blur(10px);
  }

  .api-key-section {
    margin-bottom: 24px;
  }

  .label-text {
    font-weight: 600;
    color: #fff;
    font-size: 0.95rem;
  }

  .input-field {
    width: 100%;
    margin-top: 8px;
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

  .conversation-container {
    min-height: 300px;
    max-height: 500px;
    overflow-y: auto;
    margin-bottom: 24px;
    padding: 16px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 0;
  }

  .empty-state {
    text-align: center;
    padding: 60px 20px;
    color: #888;
  }

  .messages {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .message {
    display: flex;
    gap: 12px;
    animation: fadeIn 0.3s ease-in;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .message.user {
    flex-direction: row-reverse;
  }

  .message-avatar {
    font-size: 0.75rem;
    font-weight: 700;
    flex-shrink: 0;
    color: #888;
  }

  .message-content {
    background: rgba(255, 255, 255, 0.05);
    padding: 12px 16px;
    border-radius: 0;
    max-width: 80%;
    line-height: 1.6;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .message.user .message-content {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }

  .message.assistant .message-content {
    background: rgba(100, 181, 246, 0.1);
    border: 1px solid rgba(100, 181, 246, 0.2);
    color: #e0e0e0;
  }

  .error-message {
    margin-bottom: 16px;
    padding: 12px 16px;
    background: rgba(244, 67, 54, 0.2);
    color: #ff5252;
    border: 1px solid rgba(244, 67, 54, 0.3);
    border-radius: 0;
    font-size: 0.95rem;
  }

  .input-section {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .query-input {
    width: 100%;
    padding: 12px 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 0;
    font-size: 1rem;
    font-family: inherit;
    resize: vertical;
    color: #fff;
    transition: all 0.2s;
  }

  .query-input:focus {
    outline: none;
    border-color: #64b5f6;
    background: rgba(255, 255, 255, 0.08);
  }

  .query-input:disabled {
    background: rgba(0, 0, 0, 0.3);
    cursor: not-allowed;
  }

  .button-group {
    display: flex;
    gap: 12px;
  }

  .ask-btn {
    flex: 1;
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

  .ask-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .clear-btn {
    padding: 14px 20px;
    background: rgba(255, 255, 255, 0.1);
    color: #e0e0e0;
    border: none;
    border-radius: 0;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
  }

  .clear-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
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
</style>
