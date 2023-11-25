<template>
    <h1 class="default">Default layout</h1>
    <a>{{sum}}</a>
    <slot />
</template>

<script>

    var sum = "sum";

</script>

<style>

    .default {
        background-color: gray;
    }

</style>