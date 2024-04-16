<script>
	import { RemoteRunnable } from '@langchain/core/runnables/remote';

	var result = '';
	const remoteChain = new RemoteRunnable({
		url: 'http://localhost:8000/agent'
	});

	async function getAnswer() {
		result = await remoteChain.invoke({
			input: 'This is a test'
		});
	}

	console.log(result);
</script>

<button on:click={getAnswer}></button>
