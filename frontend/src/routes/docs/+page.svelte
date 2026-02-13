<script>
  let selectedLanguage = "curl";
</script>

<main>
  <div class="docs-container">
    <header class="docs-header">
      <h1>API Documentation</h1>
      <p class="subtitle">
        Build powerful RAG applications with our REST API. Simple, fast, and
        scalable.
      </p>
    </header>

    <section class="section">
      <h2>Authentication</h2>
      <p>
        All API requests require authentication using an API key. Include your
        API key in the <code>Authorization</code> header as a Bearer token.
      </p>
      <div class="code-block">
        <pre><code>Authorization: Bearer YOUR_API_KEY</code></pre>
      </div>
      <div class="note">
        <strong>Note:</strong> Keep your API keys secure. Do not expose them in client-side
        code or public repositories.
      </div>
    </section>

    <section class="section">
      <h2>Base URL</h2>
      <p>All API endpoints are relative to the base URL:</p>
      <div class="code-block">
        <pre><code>https://your-domain.com/api</code></pre>
      </div>
    </section>

    <section class="section">
      <h2>Endpoints</h2>

      <div class="endpoint">
        <h3>Chat</h3>
        <div class="method-path">
          <span class="method post">POST</span>
          <span class="path">/chat</span>
        </div>
        <p>
          Send a query to chat with your ingested documents using RAG (Retrieval
          Augmented Generation).
        </p>

        <h4>Request Body</h4>
        <table class="params-table">
          <thead>
            <tr>
              <th>Parameter</th>
              <th>Type</th>
              <th>Required</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>query</code></td>
              <td>string</td>
              <td>Yes</td>
              <td>The question or prompt to send</td>
            </tr>
            <tr>
              <td><code>stream</code></td>
              <td>boolean</td>
              <td>No</td>
              <td>Enable streaming response (default: false)</td>
            </tr>
          </tbody>
        </table>

        <h4>Example Request</h4>
        <div class="code-tabs">
          <div class="tabs">
            <button
              class:active={selectedLanguage === "curl"}
              on:click={() => (selectedLanguage = "curl")}>cURL</button
            >
            <button
              class:active={selectedLanguage === "javascript"}
              on:click={() => (selectedLanguage = "javascript")}
              >JavaScript</button
            >
            <button
              class:active={selectedLanguage === "python"}
              on:click={() => (selectedLanguage = "python")}>Python</button
            >
          </div>

          {#if selectedLanguage === "curl"}
            <div class="code-block">
              <pre><code
                  >curl -X POST https://your-domain.com/api/chat \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '&#123;
    "query": "What is the refund policy?",
    "stream": false
  &#125;'</code
                ></pre>
            </div>
          {:else if selectedLanguage === "javascript"}
            <div class="code-block">
              <pre><code
                  >const response = await fetch('https://your-domain.com/api/chat', &#123;
  method: 'POST',
  headers: &#123;
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  &#125;,
  body: JSON.stringify(&#123;
    query: 'What is the refund policy?',
    stream: false
  &#125;)
&#125;);

const data = await response.json();
console.log(data.answer);</code
                ></pre>
            </div>
          {:else if selectedLanguage === "python"}
            <div class="code-block">
              <pre><code
                  >import requests

response = requests.post(
    'https://your-domain.com/api/chat',
    headers=&#123;
        'Authorization': 'Bearer YOUR_API_KEY',
        'Content-Type': 'application/json'
    &#125;,
    json=&#123;
        'query': 'What is the refund policy?',
        'stream': False
    &#125;
)

data = response.json()
print(data['answer'])</code
                ></pre>
            </div>
          {/if}
        </div>

        <h4>Response</h4>
        <div class="code-block">
          <pre><code
              >&#123;
  "answer": "Our refund policy allows returns within 30 days...",
  "sources": [
    &#123;
      "document": "policies.pdf",
      "page": 5,
      "relevance": 0.92
    &#125;
  ]
&#125;</code
            ></pre>
        </div>
      </div>

      <div class="endpoint">
        <h3>Ingest Documents</h3>
        <div class="method-path">
          <span class="method post">POST</span>
          <span class="path">/ingest</span>
        </div>
        <p>
          Upload PDF documents to your knowledge base. Documents are
          automatically chunked and embedded for RAG.
        </p>

        <h4>Request Body</h4>
        <p>Multipart form data with the following field:</p>
        <table class="params-table">
          <thead>
            <tr>
              <th>Parameter</th>
              <th>Type</th>
              <th>Required</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>file</code></td>
              <td>file</td>
              <td>Yes</td>
              <td>PDF file to ingest (max size based on your plan)</td>
            </tr>
          </tbody>
        </table>

        <h4>Example Request</h4>
        <div class="code-tabs">
          <div class="tabs">
            <button
              class:active={selectedLanguage === "curl"}
              on:click={() => (selectedLanguage = "curl")}>cURL</button
            >
            <button
              class:active={selectedLanguage === "javascript"}
              on:click={() => (selectedLanguage = "javascript")}
              >JavaScript</button
            >
            <button
              class:active={selectedLanguage === "python"}
              on:click={() => (selectedLanguage = "python")}>Python</button
            >
          </div>

          {#if selectedLanguage === "curl"}
            <div class="code-block">
              <pre><code
                  >curl -X POST https://your-domain.com/api/ingest \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "file=@document.pdf"</code
                ></pre>
            </div>
          {:else if selectedLanguage === "javascript"}
            <div class="code-block">
              <pre><code
                  >const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('https://your-domain.com/api/ingest', &#123;
  method: 'POST',
  headers: &#123;
    'Authorization': 'Bearer YOUR_API_KEY'
  &#125;,
  body: formData
&#125;);

const data = await response.json();
console.log(data.message);</code
                ></pre>
            </div>
          {:else if selectedLanguage === "python"}
            <div class="code-block">
              <pre><code
                  >import requests

with open('document.pdf', 'rb') as f:
    response = requests.post(
        'https://your-domain.com/api/ingest',
        headers=&#123;
            'Authorization': 'Bearer YOUR_API_KEY'
        &#125;,
        files=&#123;'file': f&#125;
    )

data = response.json()
print(data['message'])</code
                ></pre>
            </div>
          {/if}
        </div>

        <h4>Response</h4>
        <div class="code-block">
          <pre><code
              >&#123;
  "message": "Document ingested successfully",
  "document_id": 123,
  "filename": "document.pdf",
  "chunks": 45,
  "total_chars": 12847
&#125;</code
            ></pre>
        </div>
      </div>
    </section>

    <section class="section">
      <h2>Rate Limits</h2>
      <p>
        API rate limits are based on your subscription plan. Exceeding your rate
        limit will return a <code>429 Too Many Requests</code> response.
      </p>
      <table class="params-table">
        <thead>
          <tr>
            <th>Plan</th>
            <th>Requests per Minute</th>
            <th>Monthly Character Limit</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Free</td>
            <td>10</td>
            <td>50,000</td>
          </tr>
          <tr>
            <td>Pro</td>
            <td>60</td>
            <td>1,000,000</td>
          </tr>
          <tr>
            <td>Enterprise</td>
            <td>300</td>
            <td>10,000,000</td>
          </tr>
        </tbody>
      </table>
    </section>

    <section class="section">
      <h2>Error Codes</h2>
      <p>The API uses standard HTTP response codes:</p>
      <table class="params-table">
        <thead>
          <tr>
            <th>Code</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><code>200</code></td>
            <td>Success</td>
          </tr>
          <tr>
            <td><code>400</code></td>
            <td>Bad Request - Invalid parameters</td>
          </tr>
          <tr>
            <td><code>401</code></td>
            <td>Unauthorized - Invalid API key</td>
          </tr>
          <tr>
            <td><code>429</code></td>
            <td>Too Many Requests - Rate limit exceeded</td>
          </tr>
          <tr>
            <td><code>500</code></td>
            <td>Internal Server Error</td>
          </tr>
        </tbody>
      </table>
    </section>

    <section class="section">
      <h2>Streaming Responses</h2>
      <p>
        For real-time responses, set <code>stream: true</code> in your chat request.
        The response will be sent as Server-Sent Events (SSE).
      </p>
      <div class="code-block">
        <pre><code
            >const eventSource = new EventSource(
  'https://your-domain.com/api/chat?query=...',
  &#123;
    headers: &#123;
      'Authorization': 'Bearer YOUR_API_KEY'
    &#125;
  &#125;
);

eventSource.onmessage = (event) => &#123;
  console.log(event.data);
&#125;;</code
          ></pre>
      </div>
    </section>

    <section class="section">
      <h2>Best Practices</h2>
      <ul class="best-practices">
        <li>
          <strong>Cache responses</strong> when possible to reduce API calls
        </li>
        <li>
          <strong>Handle errors gracefully</strong> with proper retry logic
        </li>
        <li>
          <strong>Monitor your usage</strong> to stay within rate limits
        </li>
        <li>
          <strong>Use streaming</strong> for better user experience with long responses
        </li>
        <li>
          <strong>Chunk large documents</strong> before ingestion for better retrieval
        </li>
      </ul>
    </section>

    <section class="section">
      <h2>Support</h2>
      <p>
        Need help? Contact our support team or check out our community forum for
        assistance with integration.
      </p>
    </section>
  </div>
</main>

<style>
  main {
    background: #f8f9fa;
    min-height: 100vh;
    padding: 2rem 1rem;
  }

  .docs-container {
    max-width: 900px;
    margin: 0 auto;
    background: white;
    padding: 3rem;
    border-radius: 0;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .docs-header {
    border-bottom: 2px solid #e9ecef;
    padding-bottom: 2rem;
    margin-bottom: 3rem;
  }

  h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
    color: #212529;
  }

  .subtitle {
    font-size: 1.125rem;
    color: #6c757d;
    margin: 0;
  }

  .section {
    margin-bottom: 3rem;
  }

  h2 {
    font-size: 1.75rem;
    margin-bottom: 1rem;
    color: #212529;
    border-bottom: 1px solid #e9ecef;
    padding-bottom: 0.5rem;
  }

  h3 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: #212529;
  }

  h4 {
    font-size: 1.125rem;
    margin: 1.5rem 0 0.75rem 0;
    color: #495057;
  }

  p {
    line-height: 1.6;
    color: #495057;
    margin-bottom: 1rem;
  }

  code {
    background: #f8f9fa;
    padding: 0.2rem 0.4rem;
    border-radius: 0;
    font-family: "Monaco", "Courier New", monospace;
    font-size: 0.875rem;
    color: #e83e8c;
  }

  .code-block {
    background: #1e1e1e;
    color: #d4d4d4;
    padding: 1.5rem;
    border-radius: 0;
    overflow-x: auto;
    margin: 1rem 0;
  }

  .code-block pre {
    margin: 0;
    font-family: "Monaco", "Courier New", monospace;
    font-size: 0.875rem;
    line-height: 1.5;
  }

  .code-block code {
    background: none;
    color: #d4d4d4;
    padding: 0;
  }

  .note {
    background: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 0;
  }

  .endpoint {
    background: #f8f9fa;
    padding: 2rem;
    border-radius: 0;
    margin-bottom: 2rem;
    border: 1px solid #dee2e6;
  }

  .method-path {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .method {
    padding: 0.25rem 0.75rem;
    border-radius: 0;
    font-weight: 600;
    font-size: 0.875rem;
    text-transform: uppercase;
  }

  .method.post {
    background: #28a745;
    color: white;
  }

  .path {
    font-family: "Monaco", "Courier New", monospace;
    font-size: 1.125rem;
    color: #212529;
  }

  .params-table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    background: white;
  }

  .params-table th,
  .params-table td {
    border: 1px solid #dee2e6;
    padding: 0.75rem;
    text-align: left;
  }

  .params-table th {
    background: #f8f9fa;
    font-weight: 600;
    color: #495057;
  }

  .params-table code {
    background: #f8f9fa;
    padding: 0.2rem 0.4rem;
  }

  .code-tabs {
    margin: 1rem 0;
  }

  .tabs {
    display: flex;
    gap: 0.5rem;
    margin-bottom: -1px;
  }

  .tabs button {
    padding: 0.5rem 1rem;
    border: 1px solid #dee2e6;
    border-bottom: none;
    background: #f8f9fa;
    cursor: pointer;
    border-radius: 0;
    color: #495057;
  }

  .tabs button.active {
    background: #1e1e1e;
    color: #d4d4d4;
    border-color: #1e1e1e;
  }

  .best-practices {
    list-style: none;
    padding: 0;
  }

  .best-practices li {
    padding: 0.75rem 0;
    border-bottom: 1px solid #e9ecef;
    line-height: 1.6;
  }

  .best-practices li:last-child {
    border-bottom: none;
  }

  .best-practices strong {
    color: #212529;
  }

  @media (max-width: 768px) {
    .docs-container {
      padding: 1.5rem;
    }

    h1 {
      font-size: 2rem;
    }

    .code-block {
      padding: 1rem;
      font-size: 0.75rem;
    }
  }
</style>
