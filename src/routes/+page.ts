import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ fetch }) => {
    const res = await fetch('');
    const { location, current } = await res.json();

    return { location, current };
};