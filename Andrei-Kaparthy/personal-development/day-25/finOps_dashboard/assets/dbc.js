/*
This clientside callback handles switching the Bootstrap theme.
It is triggered by the dark mode switch.
It finds the Bootstrap CSS link in the document's head and changes its href
to the light or dark theme URL, which are stored in the 'data-bs-theme' attributes
of the switch's parent div.
*/
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        switch_theme: function(is_dark) {
            const themeLink = document.querySelector('link[rel="stylesheet"][href*="bootstrap.min.css"]');
            const lightTheme = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css";
            const darkTheme = "https://cdn.jsdelivr.net/npm/bootswatch@5.3.2/dist/darkly/bootstrap.min.css";
            themeLink.href = is_dark ? darkTheme : lightTheme;
            return null;
        }
    }
});
