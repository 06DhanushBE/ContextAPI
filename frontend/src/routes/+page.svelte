<script>
  import { goto } from "$app/navigation";
</script>

<h1>Multi-Tenant AI Chatbot</h1>

<p>
  Build your own AI chatbot with private knowledge bases.
</p>

<div style="margin-top: 20px">
  <button on:click={() => goto("/signup")}>
    Get Started
  </button>

  <button on:click={() => goto("/login")} style="margin-left: 10px">
    Login
  </button>
</div>
