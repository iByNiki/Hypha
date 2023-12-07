class ColorMode {
    static init() {
        var cookieTheme = Cookies.get("colormode");

        if (cookieTheme == undefined && colorModeSystemDefault) {
            var mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
            if (mediaQuery.matches) cookieTheme = "dark";
            else cookieTheme = "light";
        }
        if (cookieTheme == undefined) cookieTheme = colorModeTheme;

        this.setTheme(cookieTheme);
    }
    static setTheme(theme) {

        if (theme != "dark" && theme != "light") throw "Invalid theme " + theme;

        document.querySelector(":root").setAttribute("data-theme", theme);
        colorModeTheme = theme;
        Cookies.set("colormode", theme);

    }
    static getCurrentTheme() { return colorModeTheme; }
}

ColorMode.init();