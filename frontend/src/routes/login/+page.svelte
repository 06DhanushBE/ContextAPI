<script>
  import { apiFetch } from "$lib/api";
  import { setToken } from "$lib/auth";
  import { goto } from "$app/navigation";

  let email = "";
  let password = "";
  let error = "";
  let loading = false;

  async function login() {
    error = "";
    loading = true;

    try {
      const res = await apiFetch("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });

      setToken(res.access_token);
      goto("/dashboard");
    } catch (e) {
      error = e?.message || "Login failed";
    } finally {
      loading = false;
    }
  }

  function handleKeyPress(e) {
    if (e.key === "Enter") {
      login();
    }
  }
</script>

<div class="container">
  <div class="auth-card">
    <h1>Welcome Back</h1>
    <p class="subtitle">Sign in to your account</p>

    <form on:submit|preventDefault={login}>
      <div class="form-group">
        <label for="email">Email</label>
        <input
          id="email"
          type="email"
          placeholder="you@example.com"
          bind:value={email}
          on:keypress={handleKeyPress}
          required
        />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input
          id="password"
          type="password"
          placeholder="Enter your password"
          bind:value={password}
          on:keypress={handleKeyPress}
          required
        />
      </div>

      {#if error}
        <div class="error-message">{error}</div>
      {/if}

      <button type="submit" class="primary-btn" disabled={loading}>
        {loading ? "Signing in..." : "Sign In"}
      </button>
    </form>

    <p class="footer-text">
      Don't have an account?
      <a href="/signup">Sign up</a>
    </p>
  </div>
</div>

<style>
  .container {
    max-width: 450px;
    margin: 80px auto;
    padding: 0 20px;
  }

  .auth-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0;
    padding: 40px;
    backdrop-filter: blur(10px);
    text-align: center;
  }

  h1 {
    font-size: 2rem;
    margin-bottom: 10px;
    color: #fff;
  }

  .subtitle {
    color: #b0b0b0;
    margin-bottom: 30px;
    font-size: 0.95rem;
  }

  form {
    text-align: left;
  }

  .form-group {
    margin-bottom: 20px;
  }

  label {
    display: block;
    margin-bottom: 8px;
    color: #fff;
    font-weight: 600;
    font-size: 0.9rem;
  }

  input {
    width: 100%;
    padding: 12px 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 0;
    font-size: 1rem;
    color: #fff;
    transition: all 0.2s;
  }

  input:focus {
    outline: none;
    border-color: #64b5f6;
    background: rgba(255, 255, 255, 0.08);
  }

  .error-message {
    margin-bottom: 20px;
    padding: 12px;
    background: rgba(244, 67, 54, 0.2);
    color: #ff5252;
    border: 1px solid rgba(244, 67, 54, 0.3);
    border-radius: 0;
    font-size: 0.9rem;
  }

  .primary-btn {
    width: 100%;
    padding: 14px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 0;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    margin-bottom: 20px;
  }

  .primary-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .footer-text {
    color: #b0b0b0;
    font-size: 0.9rem;
    margin-top: 20px;
  }

  .footer-text a {
    color: #64b5f6;
    text-decoration: none;
    font-weight: 600;
  }
</style>
