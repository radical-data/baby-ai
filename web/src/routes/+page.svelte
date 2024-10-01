<script lang="ts">
	import { RemoteRunnable } from '@langchain/core/runnables/remote';

	let message = '';
	let answer = '';
	let isLoading = false;

	const remoteRunnable = new RemoteRunnable({
		url: 'http://localhost:8000/agent',
		options: {
			timeout: 10000000,
			headers: {
				'Content-Type': 'application/json'
			}
		}
	});

	async function logMessage(message: string) {
		try {
			const response = await fetch('http://localhost:8000/log_message/', {
				method: 'POST',
				headers: {
					Accept: 'application/json',
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					message_text: message
				})
			});

			if (!response.ok) {
				throw new Error(`Error: ${response.statusText}`);
			}

			const data = await response.json();
			console.log('Message logged successfully:', data);
		} catch (error) {
			console.error('Error logging message:', error);
		}
	}

	async function fetchLLMResponse(message: string) {
		try {
			const stream = await remoteRunnable.stream(message);

			for await (const chunk of stream) {
				answer += chunk;
			}
		} catch (error) {
			console.error('Error with LLM stream:', error);
			answer = 'Error: Something went wrong';
		}
	}

	async function handleMessage() {
		if (!message.trim()) return;

		isLoading = true;
		answer = '';

		const logPromise = logMessage(message);
		const fetchLLMResponsePromise = fetchLLMResponse(message);

		await Promise.allSettled([logPromise, fetchLLMResponsePromise]);

		isLoading = false;
	}
</script>

<main>
	<input
		placeholder="Your message"
		bind:value={message}
		on:keydown={(event) => event.key === 'Enter' && handleMessage()}
	/>

	<button on:click={handleMessage} disabled={isLoading || !message.trim()}>
		{isLoading ? 'Thinking...' : 'Say something'}
	</button>

	{#if answer}
		<p>{answer}</p>
	{/if}
</main>

<style>
	:global(body) {
		background-color: #000000;
		color: #ffffff;
		font-family: Inter;
		display: flex;
		justify-content: center;
		align-items: center;
		min-height: 100vh;
		padding: 0;
		margin: 0;
		overflow-y: auto;
	}

	input {
		color: transparent;
		background-image: url('$lib/metallic.jpg');
		background-repeat: no-repeat;
		background-size: cover;
		background-position: center;
		background-clip: text;
		-webkit-background-clip: text;

		font-weight: Bold;
		font-size: 96px;
		border: none;
		border-bottom: 10px solid #ffffff;
		padding: 20px;
		width: 90%;
		max-width: 95vw;
		box-sizing: border-box;
		outline: none;
		word-break: break-word;

		font-family: MachineLearningFont;
	}

	p {
		max-width: 75em;
		font-size: 36px;
		line-height: 150%;
	}

	button {
		background: transparent;
		color: inherit;
		align-items: center;
		background-color: inherit;
		border: 2px solid #ffffff;
		box-sizing: border-box;
		color: #ffffff;
		cursor: pointer;
		display: inline-flex;
		font-family: inherit;
		font-size: 16px;
		font-weight: 600;
		height: 48px;
		justify-content: center;
		letter-spacing: -0.8px;
		line-height: 24px;
		min-width: 140px;
		outline: 0;
		padding: 0 17px;
		text-align: center;
		text-decoration: none;
		transition: all 0.3s;
		user-select: none;
		-webkit-user-select: none;
		touch-action: manipulation;
	}

	button:focus {
		color: #171e29;
	}

	button:hover {
		border-color: #06f;
		color: #06f;
		fill: #06f;
	}

	button:active {
		border-color: #06f;
		color: #06f;
		fill: #06f;
	}

	@media (min-width: 768px) {
		button {
			min-width: 170px;
		}
	}

	.source-quote {
		font-size: 24px;
		font-weight: normal;
	}

	.source {
		font-size: 18px; /* Smaller font than content */
		font-style: italic; /* Italicize to indicate metadata */
	}

	.key-hint {
		/* font-size: 14px; */
		/* /* color: #ccc; */
		font-style: italic; /* Italic style */
		margin-left: 5px; /* Add a little space before the hint */
	}
</style>
