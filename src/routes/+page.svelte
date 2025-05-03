<script lang="ts">
    let value = $state('');

	const socket = new WebSocket('ws://192.168.40.9:8765');

	socket.onmessage = (event) => {
        const num = 100 - (event.data / 4095 * 100)
		if (num >= 0) value = num.toLocaleString('pt-BR', {maximumFractionDigits: 2});
	};
</script>

<h1>Teste123</h1>
<p>{value}%</p>
<p>😄</p>

<style>
    
</style>