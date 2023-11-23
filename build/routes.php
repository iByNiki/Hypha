<?php

require_once "router.php";

$router = new Router();

// $router->get("/home", "dir");
// $router->run();
$router->get("404", "/pages/404.php");
$router->get("/", "/pages/index.php");
$router->get("search", "/pages/search.php");
$router->get("test", "/pages/test/index.php");
$router->get("test/test", "/pages/test/test.php");
$router->run();
?>
