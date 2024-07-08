<script lang="ts">
	import { RemoteRunnable } from '@langchain/core/runnables/remote';

	let question = '';
	let answer = '';
	let context = [];
	let streamingActive = false;
	let streamController;
	let showContext = false;
	let questionSubmitted = false;

	const remoteChain = new RemoteRunnable({
		url: 'http://localhost:8000/agent/',
		options: {
			timeout: 100000,
			headers: {
				'Content-Type': 'application/json'
			}
		}
	});

	function clearAndFocusInput() {
		question = '';
		answer = '';
		context = [];
		streamingActive = false;
		questionSubmitted = false; // Reset the submission flag
		if (streamController) {
			streamController.abort();
		}
		let textarea = document.querySelector('textarea');
		if (textarea) textarea.focus();
	}

	async function handleKeyDown(event: KeyboardEvent) {
		if (streamingActive) return;

		if (event.key === 'Enter') {
			event.preventDefault();

			const description = question.trim();
			if (description) {
				answer = '';
				questionSubmitted = true; // Set the flag when the question is submitted

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
		} else if (event.key === 'c') {
			toggleContext();
		} else if (event.key === 'n') {
			if (answer != '') {
				event.preventDefault();
				clearAndFocusInput();
			}
		} else {
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
		questionSubmitted = false; // Ensure the flag is reset here too
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

<textarea placeholder="Your question" bind:value={question} on:keydown={handleKeyDown} />

<!-- {#if questionSubmitted}
	<h1>{question}</h1>
{/if} -->

<!-- {#if !questionSubmitted}
	<input placeholder="Your question" bind:value={question} on:keydown={handleKeyDown} />
{/if} -->

{#if context.length > 0}
	<button on:click={toggleContext}>
		{showContext ? 'Hide Context ' : 'Show Context '}<span class="key-hint">(c)</span>
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
	<button on:click={handleButton}>New question <span class="key-hint">(n)</span></button>
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

	textarea,
	h1 {
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

	textarea {
		/* position: fixed; Ensure it covers the entire screen area */
		top: 0;
		left: 0;
		width: 100vw; /* Full viewport width */
		/* height: 100vh; Full viewport height */
		font-size: 4vw; /* Start with a large font size that adjusts with viewport width */
		color: transparent; /* Keeping your existing style */
		background-image: url('$lib/metallic.jpg');
		background-repeat: no-repeat;
		background-size: cover;
		background-position: center;
		background-clip: text;
		-webkit-background-clip: text;
		border: none;
		padding: 20px;
		box-sizing: border-box;
		resize: none; /* Disable manual resizing */
		outline: none;
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

	/* .hide {
		opacity: 0; /* Make the input invisible */
	/* pointer-events: none; Disable mouse interactions */
	/* position: absolute;
        top: -10000;
	} */
</style>
