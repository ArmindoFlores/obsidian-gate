
function getTitle(path) {
    const split = path.split("/");
    return split[split.length-1];
}

function getUrl(path) {
    return path + ".html";
}

function search(text) {
    const matches = [];
    for (const page of pages) {
        if (page.toLowerCase().includes(text)) {
            matches.push(page);
        }
    }
    return matches.map(
        match => ({ title: getTitle(match), url: getUrl(match) })
    );
}

function handleSearch(query) {
    const results = search(query.toLowerCase());
    const container = document.getElementById("search-results");
    container.innerHTML = "";

    if (query.length === 0 || results.length === 0) {
        container.style.display = "none";
        return;
    }
    container.style.display = "block";

    const ul = document.createElement("ul");
    for (const page of results) {
        const li = document.createElement("li");
        const a = document.createElement("a");
        a.href = page.url || (page.title + ".html");
        a.textContent = page.title || page;
        li.appendChild(a);
        ul.appendChild(li);
    }

    container.appendChild(ul);
}

var pages;
