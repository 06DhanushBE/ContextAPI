<script>
  let query = "";
  let answer = "";
  let apiKey = "";
  let error = "";

  async function ask() {
    error = "";
    answer = "";

    if (!apiKey) {
      error = "Paste your API key";
      return;
    }

    const res = await fetch(
      import.meta.env.VITE_API_BASE + "/chat",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${apiKey}`
        },
        body: JSON.stringify({ query })
      }
    );

    const data = await res.json();

    if (!res.ok) {
      error = data.detail || "Request failed";
      return;
    }

    answer = data.answer;
  }
</script>

<h1>Chat</h1>

<input
  placeholder="Paste API Key"
  bind:value={apiKey}
/>

<br /><br />

<textarea
  placeholder="Ask a question"
  bind:value={query}
/>

<br /><br />

<button on:click={ask}>Ask</button>

{#if answer}
  <p><b>Answer:</b> {answer}</p>
{/if}

{#if error}
  <p style="color:red">{error}</p>
{/if}
