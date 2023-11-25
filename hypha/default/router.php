<?php

include("filetypes.php");

class Router {

    private $urls = array();
    private $paths = array();

    public function get($url, $path) {

        $this->urls[] = '/' . trim($url, '/');
        $this->paths[] = $path;

    }

    public function run() {

        global $fileTypes;

        $requestUrl = filter_var($_SERVER['REQUEST_URI'], FILTER_SANITIZE_URL);
	    $requestUrl = strtok($requestUrl, "?");

        $found = false;

        foreach ($this->urls as $key => $value) {
            if (preg_match("#^$value$#", $requestUrl)) {
                $this->route($this->paths[$key]);
                $found = true;
            }
        }

        if (!$found && file_exists(__DIR__ . "/public" . $requestUrl)) {
            $publicPath = __DIR__ . "/public" . $requestUrl;
            $extension = pathinfo($publicPath)["extension"];

            if (array_key_exists($extension, $fileTypes)) { // Check if in file types array
                $contentType = $fileTypes[$extension];
            } else {
                if (function_exists("finfo_file")) {
                    $finfo = finfo_open(FILEINFO_MIME_TYPE);
                    $contentType = finfo_file($finfo, $publicPath);
                    finfo_close($finfo);
                } else { // For old php versions
                    $contentType = mime_content_type($publicPath);
                }
            }

            header("Content-type: " . $contentType);
            include($publicPath);
            exit();
        }

        if (!$found) {
            header("HTTP/1.0 404 Not Found");
            if (in_array("/404", $this->urls)) {
                $this->route($this->paths[array_search("404", $this->urls)]);
            } else {
                echo "<h1>404</h1>";
                echo "</p>Page not found<p>";
                exit();
            }
        }
        
    }

    public function route($path) {
        include_once __DIR__ . "$path";
    }

}

?>