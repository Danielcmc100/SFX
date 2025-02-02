<script>
  import { onMount } from 'svelte';
  let sounds = [];
  let name = '';
  let file = null;
  let hostIP = '';

  onMount(async () => {
    // hostIP = await getHostIP();
    hostIP = "192.168.3.8"
    fetchSounds();
  });

  async function fetchSounds() {
    const response = await fetch(`http://${hostIP}:8000/sfx`);
    if (response.ok) {
      sounds = await response.json();
    }
  }

  async function playSound(id) {
    await fetch(`http://${hostIP}:8000/play?audio_id=${id}`);
  }

  async function uploadSound() {
    if (name && file) {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`http://${hostIP}:8000/sfx?name=${name}`, {
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
</script>

<main>
  <h1>SFX</h1>
  <p>Sounds:</p>
  <div class="sounds"> 
    {#each sounds as sound}
      <button on:click={() => playSound(sound.id)}>{sound.name}</button>
    {/each}
  </div>

  <div class="upload-container">
    <h2>Upload a sound effect</h2>
    <input type="text" bind:value={name} placeholder="Name" />
    <input type="file" accept="audio/mp3" on:change={e => file = e.target.files[0]} />
    <button on:click={uploadSound}>Upload</button>
  </div>

</main>

<style>
  main {
    text-align: center;
    padding: 1em;
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
    margin: 0.5em;
  }


  .upload-container {
    margin-top: 2em;
    padding: 1em;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
    display: inline-block;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .sounds {
    margin-top: 2em;
    padding: 1em;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
    display: inline-block;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
</style>