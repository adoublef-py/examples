<script lang="ts">
    import { enhance } from "$app/forms"
    import type { ActionData, PageData } from "./$types"

    export let data: PageData
    // export let form: ActionData //if there are errors, print them
</script>

<ul>
    {#each data.todos as todo}
        <li>
            <p>{todo.title}</p>
            <p>{todo.description}</p>
            <form method="POST" action="?/completed" use:enhance>
                <input type="hidden" name="id" value="{todo.id}" />
                <button type="submit">Completed</button>
            </form>    
        </li>
    {/each}
</ul>

<form method="POST" action="?/create" use:enhance>
    <input name="title" required/>
    <input name="description" />
    <button type="submit">Add Todo</button>
</form>
