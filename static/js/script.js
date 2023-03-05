// ========== Main search section ========== //
function toggleSearch() {
    const searchCont = document.querySelector(".search-cont");
    //show search container
    if (searchCont.style.display === 'none') {
        searchCont.style.display = 'flex';
        // hide menu if open
        if(document.querySelector(".menu").style.display === 'flex') {
            toggleMenu();
        }
    // hide search container
    } else {
        searchCont.style.display = 'none';
    }
}

toggleSearch();
document.querySelector(".search-icon").addEventListener("click", toggleSearch);


// ========== Main menu ========== //
function toggleMenu() {
    const menu = document.querySelector(".menu");
    const icon = document.querySelector("#menu-btn .bi");
    // show menu
    if (menu.style.display === 'none') {
        menu.style.display = 'flex';
        icon.classList.remove("bi-list");
        icon.classList.add("bi-x-square");
    // hide menu
    } else {
        menu.style.display = 'none';
        icon.classList.remove("bi-x-square");
        icon.classList.add("bi-list");
    }
}

toggleMenu();
document.querySelector("#menu-btn").addEventListener("click", toggleMenu);


// ========== Top Swiper ========== //
const top_swiper = new Swiper(".top-swiper", {
    loop: true,
    pagination: {
        el: ".top-swiper-pagination",
        type: "progressbar",
    },
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    autoplay: {
        delay: 3000,
        disableOnInteraction: false,
        pauseOnMouseEnter: true,
    },
    effect: 'fade',
    fadeEffect: {
        crossFade: true
    },
});


// ========== Category Swiper ========== //
const category_swiper = new Swiper(".category-swiper", {
    loop: true,
    pagination: {
        el: ".category-swiper-pagination",
        clickable: true,
    },
    autoplay: {
        delay: 5000,
        disableOnInteraction: false,
    },
});


// ========== Handle unloaded images ========== //
all_images_are_loaded = false;

function _isImageLoaded(img) {
    return img.complete && img.naturalHeight !== 0;
}

function checkImages() {
    let tries = 0;
    let check_interval = setInterval(() => {
        console.log("Checking images...");
        const images = document.querySelectorAll("img");

        allLoaded = true;
        images.forEach((img) => {
            if (!_isImageLoaded(img)) {
                allLoaded = false;
                src = img.src;
                console.log(`'${src}' is not loaded | reloading again...`);
                img.src = src + '?' + new Date().getTime();
            }
        });
        tries += 1;
        if (allLoaded) {
            clearInterval(check_interval);
            console.log("All images are loaded!");
        }
        if (tries > 5) {
            clearInterval(check_interval);
            console.log("Failed to load images after 5 tries!");
        }
    }, 5000);
}

checkImages();

// // ========== Handle active menu ========== //
// function handleActiveMenu() {
//     const menu = document.querySelector(".menu");
//     if (menu.style.display === 'flex') {
//         toggleMenu();
//     }
// }

// document.body.addEventListener("click", handleActiveMenu, true);


// ========== Handle redirection ========== //
window.addEventListener("load", () => {
    document.getElementById('login').href = "/login/?next=" + window.location.pathname;
});