var hypha = new Object();

/* HYPHA CLASS */

hypha.initialized = true;
hypha.loadPage = (url) => {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url);

    xhr.onload = () => {

        if (xhr.status != 200) return;

        window.history.pushState({"html": xhr.response.html}, "", url);

        document.open();
        document.write(xhr.response);
        document.close();

        var loadEvent = new CustomEvent("hyphaLoad");
        document.dispatchEvent(loadEvent);

    }

    xhr.send();
}

hypha.monitoredVars = [];

hypha.injectListeners = () => {

    // Hypha attributes
    var hyphaElems = document.querySelectorAll("[h-to]");
    
    for (let i = 0; i < hyphaElems.length; i++) {
        var elem = hyphaElems[i];
        elem.addEventListener("click", (event) => {
            hypha.loadPage(event.target.getAttribute("h-to"));
        });
    }


    // Reactive elements

    const reactiveParamRe = /{{.*?}}/g;
    var allElems = document.getElementsByTagName("*");
    for (let i = 0; i < allElems.length; i++) {
        var elem = allElems[i];

        // TODO: Check in attributes

        // Reactive vars in innerhtml
        if (elem.children.length == 0) {
            var re = reactiveParamRe.exec(elem.innerHTML);
            if (re != null) re.forEach((res) => {
                var varName = res.substring(2, res.length - 2);

                var type = eval("typeof(" + varName + ")");

                if (type == "undefined") {
                    console.error("Undefined variable " + res);
                    return;
                }

                var evaulation = eval(varName);

                hypha.monitoredVars.push({
                    "name": varName,
                    "elem": elem,
                    "initialInner": elem.innerHTML,
                    "last": evaulation
                });

                elem.innerHTML = elem.innerHTML.replace(res, evaulation);

            });
        }
    }

    if (hypha.monitoredVars.length > 0) {
        hypha.reactiveInterval = setInterval(hypha.checkReactiveVariables, 200);
        
        Object.keys(window).forEach(key => {
            if (/^on/.test(key)) {
                window.addEventListener(key.slice(2), event => {
                    setTimeout(hypha.checkReactiveVariables, 1);
                });
            }
        });
    }
}

hypha.checkReactiveVariables = () => {
    for (var i = 0; i < hypha.monitoredVars.length; i++) {
        var cVar = hypha.monitoredVars[i];
        var varName = cVar.name;
        var evaulation = eval(varName);
        if (evaulation != cVar.last) {
            cVar.elem.innerHTML = cVar.initialInner.replace("{{" + varName + "}}", evaulation);
            hypha.monitoredVars[i].last = evaulation;
        }
    }
}

hypha.getId = (element) => {
    return element.getAttribute("h-id");
}

hypha.getScopePrefix = (element) => {
    return hypha.getId(element) + "-";
}

hypha.getScopedClass = (element, className) => {

    return hypha.getScopePrefix(element) + className;

}

hypha.routeParams = {};
hypha.addRouteParams = (params) => {

    for (let i = 0; i < params.length; i++) {
        hypha.routeParams[params[i][0]] = params[i][1].replace("/", "");
    }

}

/* HYPHA CLASS */

window.addEventListener("load", (event) => {
    var loadEvent = new CustomEvent("hyphaLoad");
    document.dispatchEvent(loadEvent);
});

document.addEventListener("hyphaLoad", (event) => {
    hyphaInit();
    var endLoadEvent = new CustomEvent("hyphaEndLoad");
    document.dispatchEvent(endLoadEvent);
});

function hyphaInit() {

    if (hypha.initialized == true) {
        hypha.injectListeners();
        return;
    }

    hypha.injectListeners();

}

function require(text) {} // Dummy function