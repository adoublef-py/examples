<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>

<button on:click={healthCheck}>click me!</button>

<script>
    async function healthCheck() {
        const response = await fetch("http://localhost:8000/health");
        const data = await response.json();
        console.log(data);
    }
</script>