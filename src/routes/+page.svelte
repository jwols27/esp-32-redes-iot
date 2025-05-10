<script lang="ts">
	import type { PageProps } from './$types';

	let value: number = $state(0);
	let { data: clima }: PageProps = $props();

	const dataHorario = new Date();

	const socket = new WebSocket('ws://192.168.119.9:8765');
	socket.onmessage = (event) => {
		const num = 100 - (event.data / 4095) * 100;
		if (num >= 0) value = num;
	};

	let cor = $derived(value < 25 ? 'orange' : 'green');
</script>

<p>
	{dataHorario}

</p>
<p>
	{clima.location.name},
	{clima.location.region}
	-
	{clima.location.country}
</p>
<p>{clima.current.condition.text} - {clima.current.humidity}% de umidade</p>

<label for="umidade"><span style:color={cor}>{value.toLocaleString('pt-BR', { maximumFractionDigits: 2 })}%</span> de umidade</label>
<br/>
<progress id="umidade" {value} max="100"> 32% </progress> 


<style>
</style>
