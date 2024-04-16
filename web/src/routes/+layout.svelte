<svelte:head>
	<title>Baby AI</title>
	<!-- CSS Reset -->
	<link
		rel="stylesheet"
		href="https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.css"
	/>
</svelte:head>

<main>
	<slot />
</main>

<style>
	:global(body) {
		background-color: #000000;
        color: #ffffff;
        height: 100vh;
		font-family: Inter;
	}
</style>
