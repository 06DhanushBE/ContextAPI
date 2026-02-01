<script>
  import { apiFetch } from "$lib/api";
  import { setToken } from "$lib/auth";
  import { goto } from "$app/navigation";

  let email = "";
  let password = "";
  let error = "";

  async function login() {
    try {
      const res = await apiFetch("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password })
      });

      setToken(res.access_token);
      goto("/dashboard");
    } catch (e) {
      error = e.message;
    }
  }
</script>

<h1>Login</h1>

<input placeholder="Email" bind:value={email} />
<input placeholder="Password" type="password" bind:value={password} />
<button on:click={login}>Login</button>

{#if error}<p style="color:red">{error}</p>{/if}
