import MoonVector from './MoonVector.svelte';
import SunVector from './SunVector.svelte';
import PartlyCloudyNightVector from './PartlyCloudyNightVector.svelte';
import PartlyCloudyDayVector from './PartlyCloudyDayVector.svelte';
import CloudyDayVector from './CloudyDayVector.svelte';
import CloudyNightVector from './CloudyNightVector.svelte';
import FogVector from './FogVector.svelte';
import LightRainVector from './LightRainVector.svelte';
import ModerateRainVector from './ModerateRainVector.svelte';
import HeavyRainIcon from './HeavyRainIcon.svelte';
import ThunderyVector from './ThunderyVector.svelte';
import LightSnowVector from './LightSnowVector.svelte';
import HeavySnowVector from './HeavySnowVector.svelte';
import ThunderstormVector from './ThunderstormVector.svelte';
import SleetVector from './SleetVector.svelte';
import type { Component } from 'svelte';

const getWeatherIcon = (code: number): Component => {
	const horario = new Date().getHours();
	const noite = horario < 5 || horario >= 18;

	switch (code) {
		case 1000:
			return noite ? MoonVector : SunVector; // Clear/Sunny

		case 1003:
			return noite ? PartlyCloudyNightVector : PartlyCloudyDayVector; // Partly Cloudy
		case 1006:
		case 1009:
			return noite ? CloudyNightVector : CloudyDayVector; // Cloudy / Overcast

		case 1030:
		case 1135:
		case 1147:
			return FogVector; // Mist/Fog

		case 1063:
		case 1150:
		case 1153:
		case 1180:
		case 1183:
		case 1240:
		case 1273:
		case 1072:
		case 1168:
		case 1171:
		case 1198:
		case 1201:
			return LightRainVector; // Light rain, drizzle, patchy rain with thunder, freezing rain or drizzle

		case 1186:
		case 1189:
			return ModerateRainVector; // Moderate rain
		case 1192:
		case 1195:
		case 1243:
		case 1246:
			return HeavyRainIcon; // Heavy rain
		case 1276:
			return ThunderstormVector;

		case 1066:
		case 1210:
		case 1213:
		case 1255:
		case 1279:
			return LightSnowVector; // Light snow or patchy light snow with thunder

		case 1216:
		case 1219:
		case 1222:
		case 1225:
		case 1258:
		case 1282:
			return HeavySnowVector; // Moderate to heavy snow or with thunder

		case 1069:
		case 1204:
		case 1207:
		case 1249:
		case 1252:
		case 1237:
		case 1261:
		case 1264:
			return SleetVector; // Sleet or ice pellets

		case 1087:
			return ThunderyVector; // Thundery outbreaks

		default:
			return noite ? MoonVector : SunVector;
	}
};

export { getWeatherIcon, SunVector, MoonVector };
