<script lang="ts">
	import { RemoteRunnable } from '@langchain/core/runnables/remote';

	let question = '';
	let answer = '';
	let context = [];
	let streamingActive = false;
	let streamController;
	let showContext = false;

	const remoteChain = new RemoteRunnable({
		url: 'http://localhost:8000/agent/',
		options: {
			timeout: 100000,
			headers: {
				'Content-Type': 'application/json'
			}
		}
	});

	async function handleKeyDown(event: KeyboardEvent) {
		if (event.key !== 'Enter' || streamingActive) return;
		event.preventDefault();

		const description = question.trim();
		if (description) {
			answer = '';

			try {
				const stream = await remoteChain.stream({
					input: description,
					config: {}
				});

				for await (const chunk of stream) {
					if (chunk.answer) {
						answer = answer + chunk.answer;
					} else if (chunk.context) {
						context = chunk.context;
					} else {
						console.log('Received unrecognised data:', chunk);
					}
				}
			} catch (error) {
				console.error('Error:', error);
			}
		}
	}

	function handleButton() {
		if (streamingActive && streamController) {
			streamController.abort();
		}
		question = '';
		answer = '';
		context = [];
		streamingActive = false;
	}

	function toggleContext() {
		showContext = !showContext;
	}

	function extractSourceName(sourcePath: string): string {
		const parts = sourcePath.split('/');
		const fileName = parts[parts.length - 1];
		return fileName.split('.')[0];
	}
</script>

<input placeholder="Your question" bind:value={question} on:keydown={handleKeyDown} />

{#if context.length > 0}
	<button on:click={toggleContext}>
		{showContext ? 'Hide Context' : 'Show Context'}
	</button>
{/if}

{#if showContext}
	{#each context as ctx}
		<div>
			<p class="source-quote">{ctx.pageContent}</p>
			<p class="source">Source: {extractSourceName(ctx.metadata.source)}</p>
		</div>
	{/each}
{/if}

<p>{answer}</p>

{#if question != '' && answer != ''}
	<button on:click={handleButton}>Clear</button>
{/if}

<style>
	:global(body) {
		background-color: #000000;
		color: #ffffff;
		font-family: Inter;
		/* font-family: MachineLearningFont; */
		display: flex;
		justify-content: center;
		align-items: center;
		min-height: 100vh;
		padding: 0;
		margin: 0;
		overflow-y: auto;
	}

	input {
		/* color: inherit; */
		/* background: transparent; */
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
		max-width: 800px;
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
</style>
