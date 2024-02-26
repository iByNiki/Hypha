<?php

function loc($stringKey) {
    if (isset($_SERVER["HTTP_ACCEPT_LANGUAGE"]))
        $lang = substr($_SERVER["HTTP_ACCEPT_LANGUAGE"], 0, 2);
    else
        $lang = "en";

    {{payload}}

    echo $langData[$lang][$stringKey];
}

?>