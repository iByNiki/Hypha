<template>
    <HyphaLink to="||to||" class="button">
        <slot />
    </HyphaLink>
</template>

<script>



</script>

<style scoped="true">
    .button {

        cursor: pointer;
        color: #fff;
        background-color: #6A994E;
        padding: 1em;
        padding-top: .5em;
        padding-bottom: .5em;
        border-radius: 500px;
        box-shadow: 0px 0px 10px 1px rgba(0, 0, 0, .25);
        transition: background-color ease-in-out .1s;
        text-decoration: none;
        user-select: none;

    }
</style>