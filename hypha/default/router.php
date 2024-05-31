<?php

include("filetypes.php");

class Router {

    private $PARAM_REGEX = "/\[.*\]/i";

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
        $explodedUrl = explode("/", $requestUrl);

        $found = false;

        foreach ($this->urls as $key => $value) {
            $params = array(); // Clear params

            if (preg_match($this->PARAM_REGEX, $value)) {

                $explodedVal = explode("/", $value);
                
                if (count($explodedVal) == count($explodedUrl)) {
                    foreach ($explodedVal as $expKey => $expValue) {
                        if (!(str_starts_with($expValue, "[") && str_ends_with($expValue, "]"))) {
                            if ($explodedUrl[$expKey] != $explodedVal[$expKey]) break;
                            continue;
                        }

                        $paramName = substr($expValue, 1, -1);
                        $params[$paramName] = $explodedUrl[$expKey];
                        $explodedUrl[$expKey] = $expValue;
                        $newUrl = implode("/", $explodedUrl);
                        $args = array(
                            "params" => $params
                        );

                        if ($newUrl == $value) {
                            $this->route($this->paths[$key], $args);
                            $found = true;
                        }

                    }
                }

            }

            if ($requestUrl == $value && !$found) {
                $this->route($this->paths[$key], array());
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
            readfile($publicPath);
            exit();
        }

        if (!$found) {
            header("HTTP/1.0 404 Not Found");
            if (in_array("/404", $this->urls)) {
                $this->route($this->paths[array_search("404", $this->urls)], array());
            } else {
                echo "<h1>404</h1>";
                echo "</p>Page not found<p>";
                exit();
            }
        }
        
    }

    public function route($path, $request) {
        include_once __DIR__ . "$path";
    }

}

?>