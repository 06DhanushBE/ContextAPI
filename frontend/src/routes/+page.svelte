<script>
  import { goto } from "$app/navigation";
</script>

<div class="container">
  <div class="hero">
    <h1>Multi-Tenant RAG as a Service</h1>
    <p class="subtitle">
      Build your own AI chatbot with private knowledge bases. Isolated, secure,
      and blazingly fast.
    </p>

    <div class="features">
      <div class="feature">
        <h3>Isolated Knowledge Bases</h3>
        <p>Each API key has its own secure document store</p>
      </div>
      <div class="feature">
        <h3>Multi-LLM Support</h3>
        <p>Choose between Groq (cloud) or OpenAI</p>
      </div>
      <div class="feature">
        <h3>Production Ready</h3>
        <p>Rate limiting, authentication, and vector search built-in</p>
      </div>
    </div>

    <div class="cta-buttons">
      <button class="primary-btn" on:click={() => goto("/signup")}>
        Get Started
      </button>
      <button class="secondary-btn" on:click={() => goto("/login")}>
        Login
      </button>
      <button class="secondary-btn" on:click={() => goto("/docs")}>
        Documentation
      </button>
    </div>
  </div>
</div>

<style>
  .container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 60px 20px;
    text-align: center;
  }

  .hero {
    padding: 40px 0;
  }

  h1 {
    font-size: 3rem;
    margin-bottom: 20px;
    color: #fff;
    font-weight: 700;
  }

  .subtitle {
    font-size: 1.25rem;
    color: #b0b0b0;
    margin-bottom: 60px;
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
  }

  .features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 30px;
    margin-bottom: 60px;
  }

  .feature {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0;
    padding: 30px;
    backdrop-filter: blur(10px);
  }

  .feature h3 {
    color: #64b5f6;
    margin-bottom: 10px;
    font-size: 1.2rem;
  }

  .feature p {
    color: #b0b0b0;
    font-size: 0.95rem;
    line-height: 1.6;
  }

  .cta-buttons {
    display: flex;
    gap: 20px;
    justify-content: center;
    flex-wrap: wrap;
  }

  .primary-btn {
    padding: 16px 40px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 0;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
  }

  .secondary-btn {
    padding: 16px 40px;
    background: rgba(255, 255, 255, 0.1);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 0;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
  }

  @media (max-width: 768px) {
    h1 {
      font-size: 2rem;
    }

    .subtitle {
      font-size: 1rem;
    }
  }
</style>
