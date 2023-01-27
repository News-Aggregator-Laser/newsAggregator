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
            <h3><a href="/article/${article.id}">${_truncate_text(article.title, 150)}</a></h3>
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
            <h3><a href="/article/${article.id}">${_truncate_text(article.title, 150)}</a></h3>
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
        <h2>Sorry! Nothing to show here...</h2>
    </section>
    `
}
// ==================== Main ==================== //
function render_news(articles) {
    var htmlCode = "";

    if (_articles_container) {
        articles.forEach((article) => htmlCode += _generate_article_component(article));
        _articles_container.innerHTML = htmlCode ? htmlCode : _generate_empty_page_content();
    } else if (_history_articles_container) {
        articles.forEach((article) => htmlCode += _generate_history_article_component(article));
        _history_articles_container.innerHTML = htmlCode ? htmlCode : _generate_empty_page_content();
    }
}

// ==================== Run ==================== //
if (_articles_container || _history_articles_container) {
    console.log(articles);
    render_news(articles);
}