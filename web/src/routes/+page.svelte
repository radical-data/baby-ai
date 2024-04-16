<script lang="ts">
	let question = '';
	let answer = '';

	async function handleKeyDown(event: KeyboardEvent) {
		if (event.key !== 'Enter') return;
		event.preventDefault();

		const description = question.trim();
		if (description) {
			try {
				const response = await fetch('http://localhost:8000/agent/invoke', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({ input: { input: description }, config: {} })
				});
				const result = await response.json();
				console.log(result);
				answer = result.output.answer;
			} catch (error) {
				console.error('Error:', error);
			}
		}
	}

	function handleButton() {
		question = '';
		answer = '';
	}
</script>

<input placeholder="Your question" bind:value={question} on:keydown={handleKeyDown} />

<p>{answer}</p>

{#if question != '' && answer != ''}
	<button on:click={handleButton}>Clear</button>
{/if}

<style>
	:global(body) {
		display: flex;
		justify-content: center;
		align-items: center;
		height: 100vh;
		padding: 0;
		margin: 0;
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
</style>
