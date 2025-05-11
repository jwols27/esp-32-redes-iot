<script lang="ts">
	import type { PageProps } from './$types';
	import { type Component, onMount } from 'svelte';
	import { getMunicipioCorrigido, getUfSigla } from '$lib';
	import { getWeatherIcon, MoonVector, SunVector } from '$lib/vectors';

	let { data }: PageProps = $props();
	const { clima } = data;
	const WeatherIcon: Component = getWeatherIcon(clima.current.condition.code);

	let escuro: boolean = $state(true);

	onMount(() => {
		escuro = localStorage.getItem('tema') === 'escuro';
	});

	let value: number = $state(0);
	let cor = $derived(value < 25 ? 'var(--red)' : 'var(--foam)');
	let flor = $derived(value < 25 ? 'flor triste.png' : 'flor feliz.png');

	const dataHorario = new Date().toLocaleDateString('pt-BR', {
		weekday: 'long',
		year: 'numeric',
		month: 'long',
		day: 'numeric'
	});

	$effect(() => {
		document.documentElement.classList.toggle('escuro', escuro);
		localStorage.setItem('tema', escuro ? 'escuro' : 'claro');
	});

	const socket = new WebSocket('ws://192.168.119.9:8765');
	socket.onmessage = (event) => {
		const num = 100 - (event.data / 4095) * 100;
		if (num >= 0) value = num;
	};
</script>

<h1 style="margin-bottom: 0">Umidade da sua plantinha 🌻</h1>
<main>
	<section id="status" class="card flex-col center">
		<img src={flor} alt="flor" fetchPriority="high" />
		<label for="umidade">
			<b style:color={cor}>{value.toLocaleString('pt-BR', { maximumFractionDigits: 2 })}%</b>
			<span> de umidade</span></label
		>
		<br />
		<progress id="umidade" {value} max="100" style:--cor-barra={cor}></progress>
	</section>
	<section id="clima" class="card flex-col center">
		<div class="flex-col center">
			<WeatherIcon />
			<span style="font-size: 1.25em">
				{getMunicipioCorrigido(clima.location.name)} - {getUfSigla(clima.location.region)}
			</span>
			<span style="font-size: 1em">
				{dataHorario}
			</span>
		</div>
		<div class="flex-col center">
			<b style="font-size: 1.25em">Umidade {clima.current.humidity}%</b>
			<b style="font-size: 1.15em">{clima.current.condition.text}</b>
		</div>
	</section>
</main>
<footer class="card">
	<span>Ana Paula Rampanelli • Eduardo Copati • Júlia Patricia Wolschick</span>
	<button type="button" style="margin-left: auto;" onclick={() => (escuro = !escuro)}>
		{#if escuro}
			<MoonVector />
		{:else}
			<SunVector />
		{/if}
	</button>
</footer>

<style>
	main {
		width: 100%;
		height: 100%;
		max-height: min(calc(100vh - 6.6rem), 500px);
		display: flex;
		align-items: stretch;
		gap: 1rem;
	}

	button {
		border: none;
		background: none;
		color: var(--pine);
		transition: all 200ms ease;
		cursor: pointer;
		height: 2rem;

		:global(svg) {
			height: 100%;
		}
		&:hover {
			color: var(--foam);
		}

		&:active {
			color: var(--text) !important;
		}
	}

	footer {
		padding: 0.5rem 1rem !important;
		flex: initial !important;
		flex-shrink: 0;
		width: 100%;
		display: flex;
		align-items: center;
	}

	#status {
		position: relative;
		font-size: 32px;
		gap: 0.25rem;
		max-height: 500px;

		img {
			height: 100%;
			margin-bottom: 1rem;
		}
	}
	@media screen and (max-height: 1000px) {
		#status img {
			height: 100%;
		}
	}
	@media screen and (max-height: 600px) {
		h1 {
			display: none;
		}
	}

	#clima {
		gap: 1.5rem;
		line-height: 1.25;
		font-size: clamp(18px, 2.5vw, 32px);
		transition: all 200ms ease;

		:global(svg) {
			height: 5em;
		}
	}

	@media screen and (max-width: 860px) {
		main {
			flex-direction: column;
			max-height: 100%;
		}

		footer {
			flex: 1 !important;
		}

		#clima {
			font-size: clamp(20px, 6vw, 32px);
		}
	}

	progress {
		width: 100%;
		height: 2rem;
		text-align: center;
		-webkit-appearance: none;
		-moz-appearance: none;
		appearance: none;
		border-radius: 50px;
		border-width: 2px;
		border-color: var(--highlight-high);
		background: var(--highlight-high);
	}
	progress::-webkit-progress-value,
	progress::-moz-progress-bar {
		border-radius: 50px;
		background: var(--cor-barra);
	}

	.card {
		padding: 1rem;
		border-radius: 12px;
		flex: 1;
		background-color: var(--surface);
		border: 2px solid transparent;
		transition: all 200ms ease;

		&:hover {
			border: 2px solid var(--pine);
		}
	}

	.flex-col {
		display: flex;
		flex-direction: column;
	}

	.center {
		align-items: center;
		justify-content: center;
	}
</style>
