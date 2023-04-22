<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>

<button on:click={handleClientSide}>Client-side</button>

<!-- forms are a way to interact with the server -->
<form on:submit|preventDefault={handleServerSide}>
    <button type="submit">Server-side</button>
</form>

<script lang="ts">
    async function handleClientSide() {
        const response = await fetch("http://localhost:8000/client-side");
        const data = await response.json();
        console.log(data);
    }

    async function handleServerSide(e: Event){
        const formEl = e.target as HTMLFormElement;

        const response = await fetch(formEl.action, {
            method: formEl.method,
        });

        const data = await response.json();
        console.log(data);
    }
</script>