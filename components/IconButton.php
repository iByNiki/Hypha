<template>
    <a class="button" href="||to||">
        <i class="bi bi-||icon||"></i>
        <span><slot/></span>
    </a>
</template>

<style scoped="true">

.button {

    background-color: var(--color-primary);

    padding-inline: 1em;
    padding-top: .5em;
    padding-bottom: .5em;

    text-decoration: none;
    user-select: none;

    border: 2px solid var(--color-primary);
    border-radius: 5px;

    transition: border-color ease-in-out .1s, background-color ease-in-out .1s, box-shadow ease-in-out .1s;

    user-select: none;
    -webkit-tap-highlight-color: transparent;

}

.button > i {
    margin-right: .5em;
}

.button:hover {

    background-color: var(--color-secondary);
    border-color: var(--color-primary);
    box-shadow: 0px 0px 5px var(--color-primary);

}

.button:active {

    background-color: var(--color-background);

}

</style>