<template>
    <a>Index.php</a>
    <Button to="/test">Nothing</Button>
    <Text text="lol"/>

    <HyphaLink to="/search">
        GOTO SEARCH!!!
    </HyphaLink>

    <p>caca = {{caca}}</p>

</template>

<script>

    console.log("first");
    var caca = "something";

</script>

<script lang="coffee" defer="true">

    fill = (container, liquid = "coffee") ->
        "Filling the #{container} with #{liquid}..."

    console.log(fill("a", "b"));

    console.log("defer");
</script>

<config>
{
    "head": [
        {
            "type": "title",
            "inner": "Homepage"
        }
    ]
}
</config>