<template>

    <RadialGradient/>

    <div class="content">

        <div class="title-wrap">
            <Title/>
        </div>

        <div class="buttons">
            <IconButton icon="github" to="https://github.com/iByNiki/Hypha">GitHub</IconButton>
            <!-- More buttons soon -->
        </div>

    </div>

    <span class="credits">Made with <i class="bi bi-music-note"></i> by <a href="https://niki.cat">Niki</a></span>

</template>

<style scoped="true">

.content {

    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;

    width: 100svw;
    height: 100svh;

}

.title-wrap {

    display: flex;
    justify-content: center;
    align-items: center;

    background-color: var(--color-secondary);
    width: 10em;
    height: 3.5em;

    margin-bottom: 2em;
    padding-inline: .5em;

}

.credits {

    position: absolute;
    
    left: .5em;
    bottom: .5em;

    filter: opacity(75%);

}

.credits > i, a {
    color: var(--color-primary);
}

body, html {
    background: none;
    overflow: hidden;
}

</style>