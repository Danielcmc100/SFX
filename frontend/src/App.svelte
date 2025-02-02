<script>
  import { onMount } from 'svelte';

  let sounds = [];

  onMount(async () => {
    try {
      const response = await fetch('http://localhost:8000/sfx');

      if (response.ok) {
        sounds = await response.json();
      } else {
      }
    } catch (error) {
    }
  });

  async function playSound(name) {
    await fetch(`http://localhost:8000/play?audio_id=${name}`);
  }
</script>

<main>
  <h1>SFX</h1>
  <p>Sounds:</p>
  {#each sounds as sound}
    <button on:click={() => playSound(sound.id)}>{sound.name}</button>
  {/each}

  <h2>AASDASD</h2>
</main>

<style>
  main {
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
  }

  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 2em;
    margin: 0.67em 0;
  }

  button {
    display: block;
    width: 100%;
    margin: 0.5em 0;
    padding: 0.5em;
    font-size: 1em;
    cursor: pointer;
  }
</style>
