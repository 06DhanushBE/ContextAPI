<script>
  import { apiFetch } from "$lib/api";
  import { setToken } from "$lib/auth";
  import { goto } from "$app/navigation";

  let email = "";
  let password = "";
  let error = "";

  async function signup() {
    error = "";

    try {
      const res = await apiFetch("/auth/signup", {
        method: "POST",
        body: JSON.stringify({ email, password })
      });

      // auto-login after signup
      setToken(res.access_token);
      goto("/dashboard");

    } catch (e) {
      error = e.message || "Signup failed";
    }
  }
</script>

<h1>Sign up</h1>

<input placeholder="Email" bind:value={email} />
<input
  placeholder="Password"
  type="password"
  bind:value={password}
/>

<button on:click={signup}>Create account</button>

{#if error}
  <p style="color:red">{error}</p>
{/if}

<p>
  Already have an account?
  <a href="/login">Login</a>
</p>
