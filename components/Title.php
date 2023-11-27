<template>
    <h1 class="title">
        <span class="cgray">&lt;</span>hypha<span class="cgray">/&gt;</span>
    </h1>
</template>

<style scoped="true">

.title {

    overflow: hidden;
    white-space: nowrap;

    border-right: 4px solid var(--color-text);

    animation:
        typing 1s steps(9, end),
        blink-caret .75s step-end infinite;
}

@keyframes typing {
    from { width: 0; }
    to { width: 5em; }
}

@keyframes blink-caret {
    from, to { border-color: transparent; }
    50% { border-color: var(--color-text); }
}

.cgray {

    color: var(--color-primary);

}

</style>