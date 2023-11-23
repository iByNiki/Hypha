<?php

class Router {

    private $urls = array();
    private $paths = array();

    public function get($url, $path) {

        $this->urls[] = '/' . trim($url, '/');
        $this->paths[] = $path;

    }

    public function run() {

        $requestUrl = filter_var($_SERVER['REQUEST_URI'], FILTER_SANITIZE_URL);
	    $requestUrl = strtok($requestUrl, "?");

        $found = false;

        foreach ($this->urls as $key => $value) {
            if (preg_match("#^$value$#", $requestUrl)) {
                $this->route($this->paths[$key]);
                $found = true;
            }
        }

        if (!$found && file_exists("public" . $requestUrl)) {
            exit();
        }

        if (!$found) {
            header("HTTP/1.0 404 Not Found");
            if (in_array("/404", $this->urls)) {
                $this->route($this->paths[array_search("404", $this->urls)]);
            } else {
                echo "Page not found";
                exit();
            }
        }
        
    }

    public function route($path) {
        include_once __DIR__ . "$path";
    }

}

?>