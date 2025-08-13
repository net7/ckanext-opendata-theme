/** Header.js BEGIN **/
/* HEADER SCRIPT - mobile management */
document.addEventListener("DOMContentLoaded", function () {
    "use strict";
    if (document.querySelector(".rtds-header")) {
        /* GLOBAL VARIABLES */
        var rootElement = document.documentElement;
        var siteHeader = document.querySelector(".rtds-header");
        var mainHeading = document.querySelector(".rtds-main-heading");
        // var breadcrumb = document.querySelector('.rtds-breadcrumb');
        var headerHeight;
        // var breadcrumbHeight;

        var mainMenuWrapper = document.getElementById("mainNavPanel");
        var headerLinkRight = document.querySelector(".rtds-header-link-right");
        var headerSocialLinks = document.querySelector(".rtds-social-links");
        var headerSecondaryNav = document.querySelector(
            ".rtds-top-bar__navigation"
        );
        var mobilePanelLastEl = document.querySelector(".is-last-element");
        var headerMainActions = document.querySelector(
            ".rtds-main-heading__actions"
        );

        var SiteMenuWrapper = document.getElementById("siteNavWrapper");

        var mobilePanelSecondLastEl = document.querySelector(".is-second-last");

        /* FUNCTIONS */

        function toggleIcon(icon) {
            if (icon.classList.contains("is-hidden")) {
                icon.classList.remove("is-hidden");
                icon.classList.add("is-visible");
            } else if (icon.classList.contains("is-visible")) {
                icon.classList.remove("is-visible");
                icon.classList.add("is-hidden");
            }
        }

        function calculateSiteHeader(header) {
            headerHeight = header.offsetHeight;
            rootElement.style.setProperty(
                "--header-offset",
                headerHeight + "px"
            );
        }

        // function calculateBreadcrumbHeader(breadcrumb) {
        //     breadcrumbHeight = breadcrumb.offsetHeight;
        //     rootElement.style.setProperty('--breadcrumb-height', breadcrumbHeight + 'px');
        // }

        function ariaExpandedToggle(target) {
            if (target.getAttribute("aria-expanded") === "false") {
                target.setAttribute("aria-expanded", "true");
            } else {
                target.setAttribute("aria-expanded", "false");
            }
        }

        function openOffCanvasMenu(button, targetMenu) {
            button.classList.toggle("is-selected");
            ariaExpandedToggle(button);
            targetMenu.classList.toggle("is-open");
            document.body.classList.toggle("rtds-overflow-hidden");
        }

        function closeMobileMenu() {
            if (document.body.classList.contains("rtds-overflow-hidden")) {
                document.body.classList.remove("rtds-overflow-hidden");
            }

            mainMenuWrapper.classList.remove("is-open");
            document
                .getElementById("mobileNavToggle")
                .setAttribute("aria-expanded", "false");
            document
                .getElementById("mobileNavToggle")
                .classList.remove("is-selected");
        }

        function wrapAndAppend(wrapperClass, elementToWrap, parentElement) {
            // Controlla se l'elemento da avvolgere è già contenuto in un wrapperDiv con la stessa classe
            var existingWrapper = elementToWrap.closest("." + wrapperClass);

            // Se l'elemento è già avvolto, utilizza il wrapper esistente anziché crearne uno nuovo
            if (existingWrapper) {
                existingWrapper.appendChild(elementToWrap);
            } else {
                // Altrimenti, crea un nuovo wrapperDiv
                var wrapperDiv = document.createElement("div");
                wrapperDiv.classList.add(wrapperClass);
                wrapperDiv.appendChild(elementToWrap);

                // Prependi il wrapperDiv al parentElement
                parentElement.appendChild(wrapperDiv);
                if (mobilePanelLastEl) {
                    parentElement.insertBefore(wrapperDiv, mobilePanelLastEl);
                } else {
                    parentElement.appendChild(wrapperDiv);
                }
            }
        }

        function unwrapAndRemove(wrapperDiv, elementToUnwrap, parentElement) {
            if (
                elementToUnwrap &&
                elementToUnwrap.parentNode === parentElement
            ) {
                parentElement.removeChild(elementToUnwrap);
            }

            if (wrapperDiv && wrapperDiv.parentNode === parentElement) {
                parentElement.removeChild(wrapperDiv);
            }
        }
        function handleResize() {
            if (window.matchMedia("screen and (max-width: 1023px)").matches) {
                var topBar = document.querySelector(".rtds-top-bar");
                var bottomBar = document.querySelector(".rtds-bottom-bar");

                /* FOR HEADER WITH NAVIGATION IN TOP BAR */
                if (topBar && topBar.contains(SiteMenuWrapper)) {
                    document
                        .querySelector(".rtds-main-heading__container")
                        .append(SiteMenuWrapper);
                }

                /* FOR HEADER WITH NAVIGATION IN BOTTOM BAR */
                if (bottomBar && bottomBar.contains(SiteMenuWrapper)) {
                    document
                        .querySelector(".rtds-main-heading__container")
                        .append(SiteMenuWrapper);
                }

                // Verifica altri elementi e le azioni che devono essere fatte su di essi
                if (headerLinkRight) {
                    wrapAndAppend(
                        "rtds-primary-navigation__module",
                        headerLinkRight,
                        mainMenuWrapper
                    );
                }

                if (headerSecondaryNav) {
                    wrapAndAppend(
                        "rtds-primary-navigation__module",
                        headerSecondaryNav,
                        mainMenuWrapper
                    );
                }

                if (headerMainActions) {
                    wrapAndAppend(
                        "rtds-primary-navigation__module",
                        headerMainActions,
                        mainMenuWrapper
                    );
                }

                if (mobilePanelSecondLastEl) {
                    wrapAndAppend(
                        "rtds-primary-navigation__module",
                        mobilePanelSecondLastEl,
                        mainMenuWrapper
                    );
                }

                if (headerSocialLinks) {
                    wrapAndAppend(
                        "rtds-primary-navigation__module",
                        headerSocialLinks,
                        mainMenuWrapper
                    );
                }

                calculateSiteHeader(mainHeading);
            } else if (
                window.matchMedia("screen and (min-width: 1024px)").matches
            ) {
                // Se la viewport è maggiore o uguale a 1024px
                var emptyNavModules = document.querySelectorAll(
                    ".rtds-primary-navigation__module:not(.is-main):empty"
                );

                emptyNavModules.forEach(function (emptyNavModule) {
                    if (
                        SiteMenuWrapper.classList.contains(
                            "is-top-nav-positioned"
                        )
                    ) {
                        var topBarContainer = document.querySelector(
                            ".rtds-top-bar__container"
                        );
                        if (topBarContainer) {
                            topBarContainer.prepend(SiteMenuWrapper);
                        }
                    }

                    if (
                        SiteMenuWrapper.classList.contains(
                            "is-bottom-nav-positioned"
                        )
                    ) {
                        var bottomBarContainer = document.querySelector(
                            ".rtds-bottom-bar__container"
                        );
                        if (bottomBarContainer) {
                            bottomBarContainer.prepend(SiteMenuWrapper);
                        }
                    }

                    if (headerSecondaryNav) {
                        unwrapAndRemove(
                            emptyNavModule,
                            headerSecondaryNav,
                            mainMenuWrapper
                        );
                    }

                    if (headerMainActions) {
                        unwrapAndRemove(
                            emptyNavModule,
                            headerMainActions,
                            mainMenuWrapper
                        );
                    }

                    if (mobilePanelSecondLastEl) {
                        unwrapAndRemove(
                            emptyNavModule,
                            mobilePanelSecondLastEl,
                            mainMenuWrapper
                        );
                    }

                    if (headerSocialLinks) {
                        unwrapAndRemove(
                            emptyNavModule,
                            headerSocialLinks,
                            mainMenuWrapper
                        );
                    }

                    if (headerLinkRight) {
                        unwrapAndRemove(
                            emptyNavModule,
                            headerLinkRight,
                            mainMenuWrapper
                        );
                    }
                });

                // Riporto headerSocialLinks nel suo posto originale
                if (headerSecondaryNav) {
                    var topBarContainer = document.querySelector(
                        ".rtds-top-bar__container"
                    );
                    if (topBarContainer) {
                        topBarContainer.prepend(headerSecondaryNav);
                    }
                }

                if (headerSocialLinks) {
                    var utilitiesArea = document.querySelector(
                        ".rtds-top-bar__utilities-area"
                    );
                    if (utilitiesArea) {
                        utilitiesArea.prepend(headerSocialLinks);
                    }
                }

                if (headerLinkRight) {
                    var utilitiesArea = document.querySelector(
                        ".rtds-top-bar__utilities-area"
                    );
                    if (utilitiesArea) {
                        utilitiesArea.prepend(headerLinkRight);
                    }
                }

                if (headerMainActions) {
                    document
                        .querySelector(".rtds-main-heading__container")
                        .append(headerMainActions);
                }

                if (mobilePanelSecondLastEl) {
                    document
                        .querySelector("#siteHeader")
                        .append(mobilePanelSecondLastEl);
                }

                calculateSiteHeader(siteHeader);
            }
        }

        window.addEventListener("resize", handleResize);
        handleResize(); // Initialize on page load

        document
            .getElementById("mobileNavToggle")
            .addEventListener("click", function (e) {
                e.preventDefault();
                openOffCanvasMenu(this, mainMenuWrapper);
                // console.log('clicked');
            });

        document.addEventListener("keyup", function (e) {
            // if (e.key === "Escape") {
            //     if (mainMenuWrapper.classList.contains('is-open')) {
            //         closeMobileMenu();
            //         if (window.getComputedStyle(document.getElementById('mobileNavToggle')).display !== 'none') {
            //             document.getElementById('mobileNavToggle').focus();
            //         }

            //         if (document.getElementById('mainMenuToggle')) {
            //             document.getElementById('mainMenuToggle').focus();
            //         }
            //     }
            // }

            if (e.key === "Escape") {
                if (mainMenuWrapper.classList.contains("is-open")) {
                    // Verifica se il focus è all'interno del menu principale
                    const isFocusInsideMainMenu =
                        SiteMenuWrapper.contains(document.activeElement) &&
                        !document.activeElement.closest(
                            ".rtds-dropdown-menu__item"
                        );

                    if (isFocusInsideMainMenu) {
                        closeMobileMenu();

                        // Se disponibile, ripristina il focus sull'elemento principale di apertura menu
                        if (document.getElementById("mobileNavToggle")) {
                            document.getElementById("mobileNavToggle").focus();
                        }
                    }
                }
            }

            // if ((e.key === 'Tab' || e.keyCode === 9) && !mainMenuWrapper.contains(e.target)) {
            //     closeMobileMenu();
            // }
        });

        document.body.addEventListener("click", function (e) {
            if (
                (!SiteMenuWrapper.contains(e.target) ||
                    document
                        .querySelector(".rtds-primary-navigation__backdrop")
                        .contains(e.target)) &&
                mainMenuWrapper.classList.contains("is-open")
            ) {
                closeMobileMenu();
            }
        });
    }
});

/* SEARCH DIALOG */
const openModal = () => {
    const modal = document.getElementById("searchModal");
    const modalContent = modal.querySelector(".rtds-modal-content");
    const header = document.querySelector(".rtds-header");

    modal.style.display = "flex";
    // modal.classList.add("rtds-z-20");
    modal.style.zIndex = "20";
    modal.setAttribute("aria-hidden", "false");
    header.classList.add("has-search-modal-open");

    // Get all the focusable elements inside the modal content
    const focusableElements =
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
    const firstFocusable = modalContent.querySelectorAll(focusableElements)[0];
    const fallbackFocusable = modalContent.querySelector(
        ".is-focusable-element"
    ); // Adjust the selector if necessary

    // If there's a focusable element, focus on it; otherwise, focus on the fallback element
    if (firstFocusable) {
        firstFocusable.focus();
    } else if (fallbackFocusable) {
        fallbackFocusable.setAttribute("tabindex", "-1");
        fallbackFocusable.focus();
    }

    if (!document.body.classList.contains("rtds-overflow-hidden")) {
        document.body.classList.add("rtds-overflow-hidden");
    }
};

const closeModal = () => {
    const modal = document.getElementById("searchModal");
    const modalContent = modal.querySelector(".rtds-modal-content");
    const previouslyFocusedElement =
        document.getElementById("searchModalTrigger");
    const header = document.querySelector(".rtds-header");

    // Remove tabindex from the fallback focusable element
    const fallbackFocusable = modalContent.querySelector(
        ".is-focusable-element"
    );
    if (fallbackFocusable) {
        fallbackFocusable.removeAttribute("tabindex");
    }

    if (document.body.classList.contains("rtds-overflow-hidden")) {
        document.body.classList.remove("rtds-overflow-hidden");
    }

    modal.style.display = "none";
    modal.setAttribute("aria-hidden", "true");
    // modal.classList.remove("rtds-z-10");
    modal.style.zIndex = "auto";
    header.classList.remove("has-search-modal-open");
    previouslyFocusedElement.focus();
};

if (document.getElementById("searchModal")) {
    document
        .getElementById("searchModalTrigger")
        .addEventListener("click", openModal);

    document.getElementById("closeModal").addEventListener("click", closeModal);

    document
        .getElementById("searchModal")
        .addEventListener("keydown", function (event) {
            const modalContent = document.querySelector(".rtds-modal-content");
            const focusableElements = modalContent.querySelectorAll(
                'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            );
            const firstFocusableElement = focusableElements[0];
            const lastFocusableElement =
                focusableElements[focusableElements.length - 1];

            if (event.key === "Tab") {
                if (
                    event.shiftKey &&
                    document.activeElement === firstFocusableElement
                ) {
                    lastFocusableElement.focus();
                    event.preventDefault();
                } else if (
                    !event.shiftKey &&
                    document.activeElement === lastFocusableElement
                ) {
                    firstFocusableElement.focus();
                    event.preventDefault();
                }
            }

            if (event.key === "Escape") {
                closeModal();
            }
        });

    // window.addEventListener('click', function (event) {
    //     const modal = document.getElementById('searchModal');
    //     if (event.target === modal) {
    //         closeModal();
    //     }
    // });
}
/** Header.js END **/

/** Card.js BEGIN **/
/* From INCLUSIVE COMPONENT LIBRARY by Heydon Pickering
 * https://inclusive-components.design/
 * card pattern:
 * https://inclusive-components.design/cards/
 * Create redundant click event on the whole card, using only
 * card heading link
 * A click handler on the card's container element
 * simply triggers the click method on the link inside it
 * Add also a delay in click, in order to detect if the user is selecting the text and not clicking
 */

const cards = document.querySelectorAll(".rtds-card.is-card-fullclickable");
Array.prototype.forEach.call(cards, (card) => {
    let down,
        up,
        link = card.querySelector(".rtds-card__title a");
    card.style.cursor = "pointer";
    card.onmousedown = (e) => {
        // Verifica se è il tasto sinistro (0)
        if (e.button === 0) {
            down = +new Date();
        }
    };
    card.onmouseup = (e) => {
        // Procedi solo se è il tasto sinistro (0)
        if (e.button === 0) {
            up = +new Date();
            if (up - down < 200) {
                link.click();
            }
        }
    };
});
/** Card.js END **/

/** Facets.js BEGIN **/
/*
 *   This content is licensed according to the W3C Software License at
 *   https://www.w3.org/Consortium/Legal/2015/copyright-software-and-document
 *
 *  From accordion pattern
 */

("use strict");

class FacetToggle {
    constructor(domNode) {
        this.rootEl = domNode;
        this.buttonEl = this.rootEl;

        const controlsId = this.buttonEl.getAttribute("aria-controls");
        this.contentEl = document.getElementById(controlsId);

        this.open = this.buttonEl.getAttribute("aria-expanded") === "true";

        // add event listeners
        this.buttonEl.addEventListener("click", this.onButtonClick.bind(this));
    }

    onButtonClick() {
        this.toggle(!this.open);
    }

    toggle(open) {
        // don't do anything if the open state doesn't change
        if (open === this.open) {
            return;
        }

        // update the internal state
        this.open = open;

        // handle DOM updates
        this.buttonEl.setAttribute("aria-expanded", `${open}`);
        if (open) {
            this.contentEl.removeAttribute("hidden");
        } else {
            this.contentEl.setAttribute("hidden", "");
        }
    }

    // Add public open and close methods for convenience
    open() {
        this.toggle(true);
    }

    close() {
        this.toggle(false);
    }
}

// init facet toggles
const facetToggles = document.querySelectorAll("button.rtds-facets__toggle");

if (facetToggles && facetToggles.length > 0) {
    facetToggles.forEach((facetToggleEl) => {
        if (facetToggleEl) {
            new FacetToggle(facetToggleEl);
        }
    });
}

/* SHOW MORE BTN */

document.querySelectorAll(".article__show-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
        if (btn.getAttribute("data-shown") === "false") {
            btn.closest(".article").setAttribute("data-expanded", "true");
            btn.setAttribute("data-shown", "true");
            btn.textContent = "Show less";
            btn.closest(".article").querySelector(".article__content").focus();
        } else {
            btn.closest(".article").setAttribute("data-expanded", "false");
            btn.setAttribute("data-shown", "false");
            btn.textContent = "Show more";
        }
    });
});

/* SHOW MORE FACETS */
document.addEventListener("DOMContentLoaded", function () {
    // Seleziona tutti i contenitori che hanno il pulsante "mostra altri"
    const facetsContainers = document.querySelectorAll(".has-show-more");

    // Verifica che esistano contenitori con la classe has-show-more
    if (!facetsContainers || facetsContainers.length === 0) {
        return; // Esci dalla funzione se non ci sono contenitori
    }

    facetsContainers.forEach((container) => {
        const showMoreBtn = container.querySelector(".rtds-btn--show-more");

        // Verifica che esista il pulsante show more
        if (!showMoreBtn) {
            return; // Salta questo container se non ha il pulsante
        }

        const labelShow = showMoreBtn.querySelector(".rtds-btn__label-show");
        const labelHide = showMoreBtn.querySelector(".rtds-btn__label-hide");
        const hiddenItems = container.querySelectorAll(
            ".rtds-facets__item.is-hideable.rtds-hidden"
        );

        // Verifica che esistano le etichette
        if (!labelShow || !labelHide) {
            return; // Salta questo container se mancano le etichette
        }

        // Inizializza aria-expanded a false
        showMoreBtn.setAttribute("aria-expanded", "false");

        showMoreBtn.addEventListener("click", () => {
            const isExpanded =
                showMoreBtn.getAttribute("data-expanded") === "true";

            if (!isExpanded) {
                // Espandi
                hiddenItems.forEach((item) => {
                    item.classList.remove("rtds-hidden");
                });

                // Cambia le etichette
                labelShow.classList.add("rtds-hidden");
                labelHide.classList.remove("rtds-hidden");

                // Manda il focus al primo elemento
                if (hiddenItems.length > 0) {
                    const firstInput = hiddenItems[0].querySelector(
                        'input[type="checkbox"]'
                    );
                    if (firstInput) {
                        firstInput.focus();
                    }
                }

                showMoreBtn.setAttribute("data-expanded", "true");
                showMoreBtn.setAttribute("aria-expanded", "true");
            } else {
                // Collassa
                hiddenItems.forEach((item) => {
                    item.classList.add("rtds-hidden");
                });

                // Ripristina le etichette
                labelShow.classList.remove("rtds-hidden");
                labelHide.classList.add("rtds-hidden");

                showMoreBtn.setAttribute("data-expanded", "false");
                showMoreBtn.setAttribute("aria-expanded", "false");
            }
        });
    });
});
/** Facets.js END **/

/** Carousel.js BEGIN **/
/* CAROUSEL
 * SPLIDE INITIALIZATION
 */
if (document.querySelector(".rtds-carousel")) {
    var splide = new Splide(".rtds-carousel", {
        perPage: 5,
        focus: 0,
        type: "loop",
        omitEnd: true,
        perMove: 1,
        gap: "1.5rem",
        breakpoints: {
            1280: {
                perPage: 4,
            },
            1024: {
                perPage: 2,
            },
            768: {
                destroy: true,
                perPage: 2,
                arrows: false,
            },
            640: {
                destroy: true,
                arrows: false,
            },
            480: {
                perPage: 1,
                arrows: false,
            },
        },
    });

    splide.mount();
}
/** Carousel.js END **/

/** Tablist.js BEGIN **/
/* TABS */
/*
 *   This content is licensed according to the W3C Software License at
 *   https://www.w3.org/Consortium/Legal/2015/copyright-software-and-document
 *
 *   File:   tabs-manual.js
 *
 *   Desc:   Tablist widget that implements ARIA Authoring Practices
 */

("use strict");

class TabsManualHorizontal {
    constructor(groupNode) {
        this.tablistNode = groupNode;

        this.tabs = [];

        this.firstTab = null;
        this.lastTab = null;

        this.tabs = Array.from(
            this.tablistNode.querySelectorAll("[role=tab].is-tab")
        );
        this.tabpanels = [];

        for (var i = 0; i < this.tabs.length; i += 1) {
            var tab = this.tabs[i];
            var tabpanel = document.getElementById(
                tab.getAttribute("aria-controls")
            );

            tab.tabIndex = -1;
            tab.setAttribute("aria-selected", "false");
            this.tabpanels.push(tabpanel);

            tab.addEventListener("keydown", this.onKeydown.bind(this));
            tab.addEventListener("click", this.onClick.bind(this));

            if (!this.firstTab) {
                this.firstTab = tab;
            }
            this.lastTab = tab;
        }

        this.setSelectedTab(this.firstTab);
    }

    setSelectedTab(currentTab) {
        for (var i = 0; i < this.tabs.length; i += 1) {
            var tab = this.tabs[i];
            if (currentTab === tab) {
                tab.setAttribute("aria-selected", "true");
                tab.removeAttribute("tabindex");
                this.tabpanels[i].classList.remove("rtds-hidden");
            } else {
                tab.setAttribute("aria-selected", "false");
                tab.tabIndex = -1;
                this.tabpanels[i].classList.add("rtds-hidden");
            }
        }
    }

    moveFocusToTab(currentTab) {
        currentTab.focus();
    }

    moveFocusToPreviousTab(currentTab) {
        var index;

        if (currentTab === this.firstTab) {
            this.moveFocusToTab(this.lastTab);
        } else {
            index = this.tabs.indexOf(currentTab);
            this.moveFocusToTab(this.tabs[index - 1]);
        }
    }

    moveFocusToNextTab(currentTab) {
        var index;

        if (currentTab === this.lastTab) {
            this.moveFocusToTab(this.firstTab);
        } else {
            index = this.tabs.indexOf(currentTab);
            this.moveFocusToTab(this.tabs[index + 1]);
        }
    }

    /* EVENT HANDLERS */

    onKeydown(event) {
        var tgt = event.currentTarget,
            flag = false;

        switch (event.key) {
            case "ArrowLeft":
                this.moveFocusToPreviousTab(tgt);
                flag = true;
                break;

            case "ArrowUp":
                this.moveFocusToPreviousTab(tgt);
                flag = true;
                break;

            case "ArrowRight":
                this.moveFocusToNextTab(tgt);
                flag = true;
                break;

            case "ArrowDown":
                this.moveFocusToNextTab(tgt);
                flag = true;
                break;

            case "Home":
                this.moveFocusToTab(this.firstTab);
                flag = true;
                break;

            case "End":
                this.moveFocusToTab(this.lastTab);
                flag = true;
                break;

            default:
                break;
        }

        if (flag) {
            event.stopPropagation();
            event.preventDefault();
        }
    }

    // Since this example uses buttons for the tabs, the click onr also is activated
    // with the space and enter keys
    onClick(event) {
        this.setSelectedTab(event.currentTarget);
    }
}

// Initialize tablist
window.addEventListener("load", function () {
    var tablistsHorizontal = document.querySelectorAll(
        "[role=tablist].is-manual"
    );
    for (var i = 0; i < tablistsHorizontal.length; i++) {
        new TabsManualHorizontal(tablistsHorizontal[i]);
    }
});
/** Tablist.js END **/

/** Sidebar collapse/expand BEGIN **/
document.addEventListener("DOMContentLoaded", function () {
    "use strict";
    if (document.querySelector(".rtds-sidebar")) {
        var sideBar = document.querySelector(".rtds-sidebar");
        var sideBarBtn = document.querySelector(".rtds-sidebar-btn");
        var sideBarBtnIcon = document.querySelector(".rtds-sidebar-btn > svg");
        var sidebarContent = document.querySelector(".rtds-sidebar-content");
        var sidebarContentWidth = document.querySelector(".rtds-sidebar-content").offsetWidth;
        sidebarContent.style.width = sidebarContentWidth + "px";
    }

    function collapseExpandSidebar() {
        if (sideBar.getAttribute("aria-expanded") === "true") {
            sidebarContent.style.width = "0px";
            sidebarContent.style.transform = "scaleX(0)";
            sidebarContent.style.opacity = "0";
            sideBarBtnIcon.style.transform = "rotate(180deg)";
            sideBar.setAttribute("aria-expanded", "false");
        } else {
            sidebarContent.style.width = sidebarContentWidth + "px";
            sidebarContent.style.transform = "scaleX(1)";
            sidebarContent.style.opacity = "1";
            sideBarBtnIcon.style.transform = "rotate(0deg)";
            sideBar.setAttribute("aria-expanded", "true");
        }
    }

    if (sideBarBtn) {
        sideBarBtn.addEventListener("click", function (e) {
            collapseExpandSidebar();
        });
    }
});
/** Sidebar collapse/expand END **/

// CKAN Facets
("use strict");

ckan.module("opendata_theme_click", function ($) {
    return {
        initialize: function () {
            this.el.on("click", this._onClick.bind(this));
        },

        _onClick: function (event) {
            event.preventDefault();
            window.location.href = this.options.url;
        },
    };
});
