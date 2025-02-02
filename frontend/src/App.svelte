<script>
  import { onMount } from 'svelte';
  let sounds = [];
  let name = '';
  let file = null;

  async function fetchSounds() {
    const response = await fetch('http://localhost:8000/sfx');
    if (response.ok) {
      sounds = await response.json();
    }
  }

  async function playSound(id) {
    await fetch(`http://localhost:8000/play?audio_id=${id}`);
  }

  async function uploadSound() {
    if (name && file) {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`http://localhost:8000/sfx?name=${name}`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        alert('File uploaded successfully');
        fetchSounds(); // Refresh the list of sounds
      } else {
        alert('Failed to upload file');
      }
    } else {
      alert('Please enter a name and select a file');
    }
  }

  onMount(fetchSounds);
</script>

<main>
  <h1>SFX</h1>
  <p>Sounds:</p>
  {#each sounds as sound}
    <button on:click={() => playSound(sound.id)}>{sound.name}</button>
  {/each}

  <h2>Upload a sound effect</h2>
  <input type="text" bind:value={name} placeholder="Name" />
  <input type="file" accept="audio/mp3" on:change={e => file = e.target.files[0]} />
  <button on:click={uploadSound}>Upload</button>
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
  }

  h2 {
    margin-top: 2em;
  }

  input {
    display: block;
    margin: 0.5em 0;
  }

  button {
    margin-top: 1em;
  }
</style>