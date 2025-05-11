import type { PageServerLoad } from './$types';
import { WEATHER_API_KEY } from '$env/static/private';

interface Location {
	name: string;
	region: string;
	country: string;
}

interface Current {
	condition: { code: number; text: string; icon: string };
	humidity: number;
}

interface Clima {
	location: Location;
	current: Current;
}

const api = `https://api.weatherapi.com/v1/current.json?key=${WEATHER_API_KEY}&q=Sao Paulo&lang=pt`;

export const load: PageServerLoad = async ({ fetch }) => {
	const res = await fetch(api);
	const clima: Clima = await res.json();

	return { clima };
};
