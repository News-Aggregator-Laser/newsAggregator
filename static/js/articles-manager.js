// articles list should be declared in Global scope
const _history_articles_container = document.querySelector(".history-dynamic-article-section");
const _articles_container = document.querySelector(".dynamic-article-section");

console.log("manager is running...");


// ==================== Helpers ==================== //
function _truncate_text(text, max_len) {
    if (text.length > max_len)
        return text.slice(0, max_len - 3) + "...";
    return text;
}

function _generate_article_component(article) {
    return `
    <div class="article">
        <div class="article-info-cont">
            <h3><a href="/article/${article.id}">${_truncate_text(article.title, 120)}</a></h3>
            <p>${_truncate_text(article.subtitle, 150)}</p>
            <br>
        </div>
        <div class="article-img-cont">
            <img src="${article.url_image}" alt="${article.title}">
            <div class="flex-container">
                <i style="margin-right:35px;"
                    class="bi ${article.favorite ? 'bi-star-fill' : 'bi-star'} favorite-btn"
                    data-post-id="${article.id}">
                    <span class="interaction-btn-tooltip">
                        ${article.favorite ? 'Remove from favorite' : 'Add To favorite'}
                    </span>
                </i>
                <i class="bi ${article.readLater ? 'bi-bookmark-fill' : 'bi-bookmark'} read-later-btn"
                    data-post-id="${article.id}">
                    <span class="interaction-btn-tooltip">
                        ${article.readLater ? 'Remove from Read-Later' : 'Add To Read-Later'}
                    </span>
                </i>
            </div>
        </div>
    </div>
    \n
    `
}

function _generate_history_article_component(article) {
    return `
    <div class="article">
        <div class="article-info-cont">
            <h3><a href="/article/${article.id}">${_truncate_text(article.title, 120)}</a></h3>
            <p>${_truncate_text(article.subtitle, 150)}</p>
            <br>
        </div>
        <div class="article-img-cont">
            <img src="${article.url_image}" alt="${article.title}">
            <i class="bi bi-x-circle history-remove-btn" data-post-id="${article.id}">
                <span class="interaction-btn-tooltip history-remove-tooltip">Remove from History</span>
            </i>
        </div>
    </div>
    \n
    `
}

function _generate_empty_page_content() {
    return `
    <section style="width: 100%; height: 100%; display: grid; place-items: center;">
        <h2 style="color: rgba(0, 0, 0, 0.6)">Nothing to show here</h2>
    </section>
    `
}

function _generate_filter_option(value, text) {
    return `<option value="${value}">${text}</option>`
}

function _generate_filter_form(id, options, options_values) {
    if (options.length == 2) {
        options = [options[1]]
        options_values = [options_values[1]]
    }
    form = `
    <form>
        <label for="${id}">${id}:</label>
        <select name="${id}" id="${id}">
    `;
    for (let i = 0; i < options.length; i++) {
        form += `<option value="${options_values[i]}">${options[i]}</option>`;
    }
    form += ` </select>
    </form>`;
    return form
}

function _findIntersection(arr1, arr2, arr3) {
    let result = [];
    for (let i = 0; i < arr1.length; i++) {
        if (arr2.includes(arr1[i]) && arr3.includes(arr1[i])) {
            result.push(arr1[i]);
        }
    }
    return result;
}

// extract unique source, author, and category names
function _extract_metadata() {
    for (article of articles) {
        if (!authors_names.includes(article.news_author))
            authors_names.push(article.news_author);
        if (!source_names.includes(article.news_source))
            source_names.push(article.news_source);
        if (!categories_names.includes(article.news_category))
            categories_names.push(article.news_category);
    }
}


// ==================== Main ==================== //
authors_names = ["all"];
source_names = ["all"];
categories_names = ["all"];

// fill the filter options with found options
function fill_filter_option() {
    _extract_metadata();
    const container = document.querySelector(".client-filter-box");
    container.innerHTML += _generate_filter_form("authors", authors_names, authors_names);
    container.innerHTML += _generate_filter_form("sources", source_names, source_names);
    container.innerHTML += _generate_filter_form("categories", categories_names, categories_names);
}

function render_news(articles) {
    var htmlCode = "";

    if (_articles_container) {
        articles.forEach((article) => htmlCode += _generate_article_component(article));
        _articles_container.innerHTML = htmlCode ? htmlCode : _generate_empty_page_content();
    } else if (_history_articles_container) {
        articles.forEach((article) => htmlCode += _generate_history_article_component(article));
        _history_articles_container.innerHTML = htmlCode ? htmlCode : _generate_empty_page_content();
    }
    console.log(`Authors: ${authors_names}`);
    console.log(`Sources: ${source_names}`);
    console.log(`Categories: ${categories_names}`);
}

// ==================== Search ==================== //
const search_btn = document.querySelector(".client-search-btn");
const search_input = document.querySelector(".client-search-input");

function toggleSearch() {
    if (search_input.style.display === 'none') {
        search_input.style.display = 'block';
    } else {
        search_input.style.display = 'none';
    }
}

function searchInNews() {
    console.log("searching...");
    let search_query = search_input.value.toLowerCase();
    let filtered_articles = articles.filter((article) => {
        return article.title.toLowerCase().includes(search_query) ||
            article.subtitle.toLowerCase().includes(search_query) ||
            article.content.toLowerCase().includes(search_query);
    });
    render_news(filtered_articles);
}

// --- Search Event Listeners ---//
search_btn.addEventListener("click", () => {
    toggleSearch();
});
search_input.addEventListener("keyup", (e) => {
    searchInNews();
});


// ==================== Filter ==================== //
const filter_btn = document.querySelector(".client-filter-btn");
const filter_box = document.querySelector(".client-filter-box");

author_filter_keyword = "all"
source_filter_keyword = "all"
category_filter_keyword = "all"

function toggleFilter() {
    if (filter_box.style.display === 'none') {
        filter_box.style.display = 'block';
    } else {
        filter_box.style.display = 'none';
    }
}

function filterNews() {
    filtered_by_author = [];
    filtered_by_source = [];
    filtered_by_category = [];
    for (article of articles) {
        if (author_filter_keyword == "all" || author_filter_keyword == article.news_author) {
            filtered_by_author.push(article);
        }
        if (source_filter_keyword == "all" || source_filter_keyword == article.news_source) {
            filtered_by_source.push(article);
        }
        if (category_filter_keyword == "all" || category_filter_keyword == article.news_category) {
            filtered_by_category.push(article);
        }
    }
    render_news(_findIntersection(filtered_by_author, filtered_by_source, filtered_by_category));
}

// --- Filter Event Listeners ---//
filter_btn.addEventListener("click", () => {
    toggleFilter();
});


// ==================== Run ==================== //
if (_articles_container || _history_articles_container) {
    toggleSearch();
    toggleFilter();
    render_news(articles);
    fill_filter_option();

    // ========== Handle active menu ========== //
    function handleActiveFilterBox() {
        if (filter_box.style.display === 'block') {
            toggleFilter();
        }
    }

    // document.body.addEventListener("click", handleActiveFilterBox, true);

    // filter by author
    const author_filter = document.querySelector("#authors");
    author_filter.addEventListener("change", (e) => {
        author_filter_keyword = e.target.value;
        filterNews();
    });

    // filter by source
    const source_filter = document.querySelector("#sources");
    source_filter.addEventListener("change", (e) => {
        source_filter_keyword = e.target.value;
        filterNews();
    });

    // filter by category
    const category_filter = document.querySelector("#categories");
    category_filter.addEventListener("change", (e) => {
        category_filter_keyword = e.target.value;
        filterNews();
    });
}