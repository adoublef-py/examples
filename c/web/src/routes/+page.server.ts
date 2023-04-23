import { fail } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";

export const load: PageServerLoad = async (e) => {
    const response = await fetch("http://localhost:8000/todos");

    return response.json();
};

export const actions: Actions = {
    completed: async ({ request }) => {
        const formData = await request.formData();

        // convert FormData to JSON
        const id = formData.get("id");

        if (!id) {
            return fail(400, { id, message: "id is required" });
        }

        const response = await fetch("http://localhost:8000/todos/" + id, {
            method: "DELETE",
        });

        return response.json();
    },
    create: async ({ request }) => {
        const formData = await request.formData();

        // convert FormData to JSON
        const body = Object.fromEntries(formData.entries());

        const response = await fetch("http://localhost:8000/todos", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
        });

        return response.json();
    }
};