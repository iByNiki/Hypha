<template>

    <div class="gradient"><div></div></div>

</template>

<style scoped="true">
.gradient {

    display: flex;
    justify-content: center;
    align-items: center;

    position: absolute;

    left: 0;
    top: 0;

    width: 100%;
    height: 100%;

    z-index: -1;

    background-color: var(--color-background);

}

.gradient > div {

    width: 800px;
    height: 800px;
    background: radial-gradient(circle, var(--color-secondary) 0%, var(--color-background) 50%);
    filter: opacity(70%);

}
</style>