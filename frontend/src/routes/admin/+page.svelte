<script>
  import { onMount } from "svelte";
  import { apiFetch } from "$lib/api.js";

  let dashboard = null;
  let error = "";

  async function loadDashboard() {
    try {
      dashboard = await apiFetch("/admin/dashboard");
    } catch (err) {
      error = err?.message || "Failed to load dashboard";
    }
  }

  async function toggleUser(userId) {
    if (!confirm("Toggle user active status?")) return;

    try {
      await apiFetch(`/admin/users/${userId}/toggle-active`, {
        method: "POST",
      });
      await loadDashboard();
    } catch (err) {
      alert("Error: " + (err?.message || "Unknown error"));
    }
  }

  async function deleteUser(userId) {
    if (!confirm("Permanently delete user and all data?")) return;

    try {
      await apiFetch(`/admin/users/${userId}`, { method: "DELETE" });
      await loadDashboard();
    } catch (err) {
      alert("Error: " + (err?.message || "Unknown error"));
    }
  }

  onMount(loadDashboard);
</script>

<main>
  <h1>Admin Dashboard</h1>

  {#if error}
    <div class="error">
      <strong>Access Denied:</strong>
      {error}
      <p>Only admin users can access this page. (Email must contain 'admin')</p>
    </div>
  {:else if !dashboard}
    <p>Loading...</p>
  {:else}
    <div class="stats">
      <div class="stat-card">
        <h3>Total Users</h3>
        <p class="stat-number">{dashboard.total_users}</p>
      </div>
      <div class="stat-card">
        <h3>Total API Keys</h3>
        <p class="stat-number">{dashboard.total_api_keys}</p>
      </div>
      <div class="stat-card">
        <h3>Total Documents</h3>
        <p class="stat-number">{dashboard.total_documents}</p>
      </div>
    </div>

    <h2>Users</h2>
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Email</th>
          <th>Status</th>
          <th>Plan</th>
          <th>API Keys</th>
          <th>Documents</th>
          <th>Usage (chars)</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {#each dashboard.users as user}
          <tr class:inactive={!user.is_active}>
            <td>#{user.id}</td>
            <td>{user.email}</td>
            <td>
              <span class="status" class:active={user.is_active}>
                {user.is_active ? "Active" : "Inactive"}
              </span>
            </td>
            <td><span class="badge">{user.plan}</span></td>
            <td>{user.api_keys_count}</td>
            <td>{user.documents_count}</td>
            <td>{user.total_usage_chars.toLocaleString()}</td>
            <td>
              <button on:click={() => toggleUser(user.id)} class="btn-toggle">
                {user.is_active ? "Deactivate" : "Activate"}
              </button>
              <button on:click={() => deleteUser(user.id)} class="btn-delete"
                >Delete</button
              >
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  {/if}
</main>

<style>
  main {
    padding: 2rem;
    max-width: 1400px;
    margin: 0 auto;
  }

  h1 {
    margin-bottom: 2rem;
  }

  .error {
    background: #fee;
    border: 2px solid #c33;
    border-radius: 0;
    padding: 1rem;
    margin: 1rem 0;
    color: #c33;
  }

  .stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 3rem;
  }

  .stat-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 0;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }

  .stat-card h3 {
    margin: 0 0 0.5rem 0;
    font-size: 0.9rem;
    opacity: 0.9;
    font-weight: 500;
  }

  .stat-number {
    font-size: 2.5rem;
    font-weight: bold;
    margin: 0;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    border-radius: 0;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  thead {
    background: #f8f9fa;
  }

  th,
  td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid #e9ecef;
  }

  th {
    font-weight: 600;
    color: #495057;
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  tbody tr.inactive {
    opacity: 0.6;
  }

  .status {
    padding: 0.25rem 0.75rem;
    border-radius: 0;
    font-size: 0.85rem;
    font-weight: 500;
  }

  .status.active {
    background: #d4edda;
    color: #155724;
  }

  .status:not(.active) {
    background: #f8d7da;
    color: #721c24;
  }

  .badge {
    background: #e7f5ff;
    color: #1971c2;
    padding: 0.25rem 0.75rem;
    border-radius: 0;
    font-size: 0.85rem;
    font-weight: 500;
    text-transform: capitalize;
  }

  button {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 0;
    cursor: pointer;
    font-size: 0.875rem;
    font-weight: 500;
    margin-right: 0.5rem;
  }

  .btn-toggle {
    background: #0d6efd;
    color: white;
  }

  .btn-delete {
    background: #dc3545;
    color: white;
  }
</style>
