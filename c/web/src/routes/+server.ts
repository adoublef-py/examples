import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ request }) => {
    const response = await fetch("http://localhost:8000/server-side");

    const data = await response.json();

    return json(data);
};