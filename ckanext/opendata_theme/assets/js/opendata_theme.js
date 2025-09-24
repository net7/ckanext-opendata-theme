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

/** side-navigation.js BEGIN **/
/*
 *   This content is licensed according to the W3C Software License at
 *   https://www.w3.org/Consortium/Legal/2015/copyright-software-and-document
 *
 *   Supplemental JS for the disclosure menu keyboard behavior
 */

'use strict';
// Helper function to find the closest ancestor with a specific tag name
function findAncestor(element, tagName) {
  while (element) {
    if (element.tagName.toLowerCase() === tagName) {
      return element;
    }
    element = element.parentElement;
  }
  return null;
}

class submenuDisclosure {
  constructor(domNode) {
    this.rootNode = domNode;
    this.parentNav = domNode.closest('.rtds-side-navigation');
    this.controlledNodes = [];
    this.openIndex = null;
    this.useArrowKeys = true;
    this.topLevelNodes = [
      ...this.rootNode.querySelectorAll(
        '.rtds-nav-link, .rtds-nav-toggle'
      ),
    ];

    this.topLevelNodes.forEach((node) => {
      // handle button + menu
      if (
        node.tagName.toLowerCase() === 'button' &&
        node.hasAttribute('aria-controls')
      ) {
        const menuLiParent = node.closest('li');
        const menu = menuLiParent.querySelector('ul');

        if (menu) {
          // save ref controlled menu
          this.controlledNodes.push(menu);

          // collapse menus
          if (menu.querySelector('.is-current') || node.classList.contains('is-current')) {
            node.setAttribute('aria-expanded', 'true');
            this.toggleMenu(menu, true);
          } else {
            node.setAttribute('aria-expanded', 'false');
            this.toggleMenu(menu, false);
          }

          // attach event listeners
          menu.addEventListener('keydown', this.onMenuKeyDown.bind(this));
          node.addEventListener('click', this.onButtonClick.bind(this));
          node.addEventListener('keydown', this.onButtonKeyDown.bind(this));
        }
      }
      // handle links
      else {
        this.controlledNodes.push(null);
        node.addEventListener('keydown', this.onLinkKeyDown.bind(this));
      }
    });

    // Gestione specifica per i sub-submenu
    const subSubmenuToggleButtons = this.rootNode.querySelectorAll('.rtds-side-navigation__sub-submenu');
    subSubmenuToggleButtons.forEach(subMenu => {
      const toggleButton = subMenu.previousElementSibling.querySelector('.rtds-nav-toggle');
      if (toggleButton) {
        toggleButton.addEventListener('click', this.onSubSubmenuToggleClick.bind(this));
      }
    });

    // MODIFICATO: Rimosso l'ascoltatore di eventi focusout/blur
    // this.rootNode.addEventListener('focusout', this.onBlur.bind(this));

    // Aggiungiamo il riferimento al toggle button principale
    this.mainMenuToggle = this.parentNav.querySelector('.rtds-nav-list-toggle');

    // Aggiungiamo il listener per l'Escape sul menu principale
    this.rootNode.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && window.innerWidth < 768) {
        // Verifichiamo se il menu principale è aperto
        if (this.mainMenuToggle && this.mainMenuToggle.getAttribute('aria-expanded') === 'true') {
          this.mainMenuToggle.setAttribute('aria-expanded', 'false');
          this.mainMenuToggle.focus();
        }
      }
    });
  }

  // Nuovo metodo per gestire i toggle dei sub-submenu
  onSubSubmenuToggleClick(event) {
    event.stopPropagation(); // Impedisce la propagazione dell'evento ai livelli superiori
    
    const button = event.currentTarget;
    const isExpanded = button.getAttribute('aria-expanded') === 'true';
    const controlledMenuId = button.getAttribute('aria-controls');
    const controlledMenu = document.getElementById(controlledMenuId);
    
    // Toggle aria-expanded
    button.setAttribute('aria-expanded', (!isExpanded).toString());
    
    // Toggle visualizzazione menu
    if (controlledMenu) {
      controlledMenu.style.display = isExpanded ? 'none' : 'block';
    }
  }

  controlFocusByKey(keyboardEvent, nodeList, currentIndex) {
    switch (keyboardEvent.key) {
      case 'ArrowUp':
      case 'ArrowLeft':
        keyboardEvent.preventDefault();
        if (currentIndex > -1) {
          var prevIndex = Math.max(0, currentIndex - 1);
          nodeList[prevIndex].focus();
        }
        break;
      case 'ArrowDown':
      case 'ArrowRight':
        keyboardEvent.preventDefault();
        if (currentIndex > -1) {
          var nextIndex = Math.min(nodeList.length - 1, currentIndex + 1);
          nodeList[nextIndex].focus();
        }
        break;
      case 'Home':
        keyboardEvent.preventDefault();
        nodeList[0].focus();
        break;
      case 'End':
        keyboardEvent.preventDefault();
        nodeList[nodeList.length - 1].focus();
        break;
    }
  }

  // public function to close open menu
  close() {
    this.toggleExpand(this.openIndex, false);
  }

  // MODIFICATO: Rimosso o commentato il metodo onBlur
  /*
  onBlur(event) {
    var menuContainsFocus = this.rootNode.contains(event.relatedTarget);
    if (!menuContainsFocus && this.openIndex !== null) {
      this.toggleExpand(this.openIndex, false);
    }
  }
  */

  onButtonClick(event) {
    var target = event.target;
    
    // Controlla se questo è un bottone di sub-submenu
    if (target.closest('.rtds-side-navigation__second-level-label')) {
      // Lascia che l'evento venga gestito da onSubSubmenuToggleClick
      return;
    }

    // Check if the target is not a button but is a descendant of a button
    if (target.tagName.toLowerCase() !== 'button') {
      var buttonAncestor = findAncestor(target, 'button');

      // If an ancestor button is found, trigger the click on that button
      if (buttonAncestor) {
        buttonAncestor.click();
        return; // Stop further processing since the click is handled
      }
    }

    var button = event.currentTarget;
    var buttonIndex = this.topLevelNodes.indexOf(button);
    var buttonExpanded = button.getAttribute('aria-expanded') === 'true';
    this.toggleExpand(buttonIndex, !buttonExpanded);
  }

  onButtonKeyDown(event) {
    var targetButtonIndex = this.topLevelNodes.indexOf(document.activeElement);

    // close on escape
    if (event.key === 'Escape') {
      this.toggleExpand(this.openIndex, false);
    }

    // move focus into the open menu if the current menu is open
    else if (
      this.useArrowKeys &&
      this.openIndex === targetButtonIndex &&
      event.key === 'ArrowDown'
    ) {
      event.preventDefault();
      this.controlledNodes[this.openIndex].querySelector('a').focus();
    }

    // handle arrow key navigation between top-level buttons, if set
    else if (this.useArrowKeys) {
      this.controlFocusByKey(event, this.topLevelNodes, targetButtonIndex);
    }
  }

  onLinkKeyDown(event) {
    var targetLinkIndex = this.topLevelNodes.indexOf(document.activeElement);

    // handle arrow key navigation between top-level buttons, if set
    if (this.useArrowKeys) {
      this.controlFocusByKey(event, this.topLevelNodes, targetLinkIndex);
    }
  }

  onMenuKeyDown(event) {
    if (this.openIndex === null) {
      return;
    }

    var menuLinks = Array.prototype.slice.call(
      this.controlledNodes[this.openIndex].querySelectorAll('a')
    );
    var currentIndex = menuLinks.indexOf(document.activeElement);

    // close on escape
    if (event.key === 'Escape') {
      this.topLevelNodes[this.openIndex].focus();
      this.toggleExpand(this.openIndex, false);
    }

    // handle arrow key navigation within menu links, if set
    else if (this.useArrowKeys) {
      this.controlFocusByKey(event, menuLinks, currentIndex);
    }
  }

  toggleExpand(index, expanded) {
    // close open menu, if applicable
    if (this.openIndex !== index) {
      this.toggleExpand(this.openIndex, false);
    }

    // handle menu at called index
    if (this.topLevelNodes[index]) {
      this.openIndex = expanded ? index : null;
      this.topLevelNodes[index].setAttribute('aria-expanded', expanded);
      this.toggleMenu(this.controlledNodes[index], expanded);
    }
  }

  toggleMenu(domNode, show) {
    if (domNode) {
      domNode.style.display = show ? 'block' : 'none';
    }
  }

  updateKeyControls(useArrowKeys) {
    this.useArrowKeys = useArrowKeys;
  }
}

/* Initialize Disclosure Menus */

window.addEventListener(
  'load',
  function () {
    const navListToggle = document.querySelector('.rtds-nav-list-toggle');
    if (navListToggle) {
      // Funzione per aggiornare aria-expanded in base alla visibilità
      //const updateAriaExpanded = () => {
      ////};

      // Gestione del click
      navListToggle.addEventListener('click', function() {
        const currentState = this.getAttribute('aria-expanded') === 'true';
        this.setAttribute('aria-expanded', (!currentState).toString());
      });

      // Gestione dello scroll
      let lastScrollTop = 0;
      window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        // Se stiamo scrollando verso l'alto e il menu è aperto
        if (scrollTop < lastScrollTop && navListToggle.getAttribute('aria-expanded') === 'true') {
          // Manteniamo il menu aperto
          navListToggle.setAttribute('aria-expanded', 'true');
        }
        lastScrollTop = scrollTop;
      });
    }

    // Inizializza i menu dropdown
    var dropdownMenus = document.querySelectorAll('.has-nav-dropdown');
    var disclosureMenus = [];

    for (var i = 0; i < dropdownMenus.length; i++) {
      disclosureMenus[i] = new submenuDisclosure(dropdownMenus[i]);
    }

    // listen to arrow key checkbox
    var arrowKeySwitch = document.getElementById('arrow-behavior-switch');
    if (arrowKeySwitch) {
      arrowKeySwitch.addEventListener('change', function () {
        var checked = arrowKeySwitch.checked;
        for (var i = 0; i < disclosureMenus.length; i++) {
          disclosureMenus[i].updateKeyControls(checked);
        }
      });
    }

  },
  false
);
/** side-navigation.js END **/

/** Sidebar collapse/expand BEGIN **/
document.addEventListener("DOMContentLoaded", function () {
    "use strict";
    var sideBar = document.querySelector(".rtds-sidebar");
    var sideBarBtn = document.querySelector(".rtds-sidebar-btn");
    var sideBarBtnIcon = document.querySelector(".rtds-sidebar-btn > svg");
    var sidebarContent = document.querySelector(".rtds-sidebar-content");
    var sidebarContentWidth;
    
    if (sideBar && sidebarContent) {
        sidebarContentWidth = sidebarContent.offsetWidth;
        sidebarContent.style.width = sidebarContentWidth + "px";
    }

    function collapseExpandSidebar() {
        if (!sideBar || !sidebarContent) return;
        
        if (sideBar.getAttribute("aria-expanded") === "true") {
            sidebarContent.style.width = "0px";
            sidebarContent.style.transform = "scaleX(0)";
            sidebarContent.style.opacity = "0";
            if (sideBarBtnIcon) {
                sideBarBtnIcon.style.transform = "rotate(180deg)";
            }
            sideBar.setAttribute("aria-expanded", "false");
        } else {
            sidebarContent.style.width = sidebarContentWidth + "px";
            sidebarContent.style.transform = "scaleX(1)";
            sidebarContent.style.opacity = "1";
            if (sideBarBtnIcon) {
                sideBarBtnIcon.style.transform = "rotate(0deg)";
            }
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

/** Form with validation BEGIN **/
document.addEventListener("DOMContentLoaded", function () {
    ///* Regex per verifica email */
    const emailRegex = /\S+@\S+\.\S+/; // has @ and .

    ///* Form */
    const elForm = document.getElementById("hasValidationForm");

    if (elForm) {
        ///* Campi form */
        const elRequiredName = document.getElementsByClassName("is-name")[0];
        const elRequiredFamilyname =
            document.getElementsByClassName("is-familyname")[0];
        const elPrivacy = document.getElementsByClassName("is-privacy")[0];
        const elEmail = document.getElementsByClassName("is-email")[0];

        ///* Errori form da verificare */
        const formErrors = {
            name: false,
            familyname: false,
            email: false,
            privacy: false,
        };

        let hasSubmitted = false;

        validateField({
            elField: elEmail,
            validateFn: validateFieldEmail,
        });

        validateField({
            elField: elRequiredName,
            validateFn: validateFieldRequired,
            errorKey: "name",
        });

        validateField({
            elField: elRequiredFamilyname,
            validateFn: validateFieldRequired,
            errorKey: "familyname",
        });

        validateField({
            elField: elPrivacy,
            validateFn: validateFieldPrivacy,
        });

        // Gestione validazione su 3 eventi: change, blur, keyup
        function validateField({ elField, validateFn, errorKey }) {
            let touched = false;

            elField.addEventListener("change", (e) => {
                touched = true; // mark it as touched so that on blur it shows the error.
                validateFn(e.target, { live: true, errorKey });
                if (hasSubmitted) {
                    updateSubmitSummary();
                }
            });

            elField.addEventListener("keyup", (e) => {
                // remove any error on keyup if existent
                validateFn(e.target, { removeOnly: true, errorKey });

                if (hasSubmitted) {
                    updateSubmitSummary();
                }
            });

            elField.addEventListener("blur", (e) => {
                if (!touched) return;
                // show error if touched
                validateFn(e.target, { live: true, errorKey });
            });
        }

        // Controllo email
        function validateFieldEmail(el, opts) {
            const isEmpty = el.value === "";
            updateFieldDOM(el, !isEmpty, "Email obbligatoria.", opts);

            if (isEmpty) {
                formErrors.email = true;
            } else {
                const isEmailValid = el.value.match(emailRegex);
                updateFieldDOM(el, isEmailValid, "Email non valida.", opts);
                formErrors.email = !isEmailValid;
            }
        }

        // Validazione campi obbligatori
        function validateFieldRequired(el, opts) {
            const isEmpty = el.value === "";
            const errorKey = opts?.errorKey;
            const elField = el.closest(".rtds-input-field");
            const elLabel = elField.querySelector(
                ".rtds-input-field__label-text"
            );
            const fieldLabel = elLabel ? elLabel.innerText : "Field";

            updateFieldDOM(el, !isEmpty, `${fieldLabel} obbligatorio.`, opts);

            if (errorKey) {
                formErrors[errorKey] = isEmpty;
            }
        }

        // Validazione campo privacy (checkbox)
        function validateFieldPrivacy(el, opts) {
            const isNotChecked = el.checked === false;
            updateFieldDOM(
                el,
                !isNotChecked,
                "Devi dichiarare di aver letto la Privacy Policy.",
                opts
            );

            formErrors.privacy = isNotChecked;
        }

        // Aggiornamento errore nel campo e gestione attributi accessibilità
        function updateFieldDOM(el, isValid, errorMessage, opts) {
            const removeOnly = opts?.removeOnly;
            const isLive = opts?.live;
            const elField = el.closest(".rtds-input-field");
            const elError = elField.querySelector(".rtds-input-field__error");

            if (isValid) {
                elField.classList.remove("is-invalid");
                elError.innerText = ""; // It's valid
                el.removeAttribute("aria-invalid");
            } else if (!removeOnly) {
                elField.classList.add("is-invalid");
                el.setAttribute("aria-invalid", "true");
                elError.setAttribute("aria-live", isLive ? "assertive" : "off");
                elError.innerText = errorMessage;
            }
        }

        // Aggiornamento feedback form a invio
        function updateSubmitSummary({ isSubmit } = {}) {
            const elSummary = elForm.querySelector(".rtds-form-feedback");
            const elSummaryMsg = elSummary.querySelector(
                ".rtds-form-feedback-msg"
            );

            // Clear form feedback
            elSummaryMsg.classList.remove("is-invalid");
            elSummaryMsg.classList.remove("is-success");
            elSummaryMsg.innerText = "";
            const errorsState = Object.entries(formErrors);

            const invalidFields = errorsState
                .filter(([key, value]) => value === true)
                .map(([key]) => {
                    const elField = elForm.querySelector(`.is-${key}`);
                    return elField ? elField.getAttribute("data-label") : key;
                });

            if (invalidFields.length > 0) {
                // Show error msg
                const errorCount = invalidFields.length;
                const errorMsg =
                    errorCount === 1
                        ? `È presente ${errorCount} campo non valido: ${invalidFields.join(
                              ", "
                          )}.`
                        : `Sono presenti ${errorCount} campi non validi: ${invalidFields.join(
                              ", "
                          )}.`;

                elSummaryMsg.classList.add("is-invalid");
                elSummaryMsg.innerText = errorMsg;

                elSummary.querySelector(".rtds-form-feedback-sr").innerText =
                    isSubmit
                        ? // Set SR error message only on submit to avoid being re-announced
                          // every time the error summary visually changes.
                          errorMsg
                        : "";
            } else if (isSubmit) {
                const successMsg = "Form inviata con successo.";
                elSummary.querySelector(".rtds-form-feedback-sr").innerText =
                    successMsg;
                elSummaryMsg.innerText = successMsg;
                elSummaryMsg.classList.add("is-success");
            }
        }

        elForm.addEventListener("submit", (e) => {
            e.preventDefault();
            hasSubmitted = true;

            // Validate again
            validateFieldEmail(elEmail);
            validateFieldRequired(elRequiredName, { errorKey: "name" });
            validateFieldRequired(elRequiredFamilyname, {
                errorKey: "familyname",
            });
            validateFieldPrivacy(elPrivacy);

            updateSubmitSummary({ isSubmit: true });
        });
    }
});
/** Form with validation END **/

/** Modal dialog BEGIN **/
/*
 *   This content is licensed according to the W3C Software License at
 *   https://www.w3.org/Consortium/Legal/2015/copyright-software-and-document
 */

'use strict';

var aria = aria || {};

aria.Utils = aria.Utils || {};

(function () {
  /*
   * When util functions move focus around, set this true so the focus listener
   * can ignore the events.
   */
  aria.Utils.IgnoreUtilFocusChanges = false;

  aria.Utils.dialogOpenClass = 'has-dialog';

  /**
   * @description Set focus on descendant nodes until the first focusable element is
   *       found.
   * @param element
   *          DOM node for which to find the first focusable descendant.
   * @returns {boolean}
   *  true if a focusable element is found and focus is set.
   */
  aria.Utils.focusFirstDescendant = function (element) {
    for (var i = 0; i < element.childNodes.length; i++) {
      var child = element.childNodes[i];
      if (
        aria.Utils.attemptFocus(child) ||
        aria.Utils.focusFirstDescendant(child)
      ) {
        return true;
      }
    }
    return false;
  }; // end focusFirstDescendant

  /**
   * @description Find the last descendant node that is focusable.
   * @param element
   *          DOM node for which to find the last focusable descendant.
   * @returns {boolean}
   *  true if a focusable element is found and focus is set.
   */
  aria.Utils.focusLastDescendant = function (element) {
    for (var i = element.childNodes.length - 1; i >= 0; i--) {
      var child = element.childNodes[i];
      if (
        aria.Utils.attemptFocus(child) ||
        aria.Utils.focusLastDescendant(child)
      ) {
        return true;
      }
    }
    return false;
  }; // end focusLastDescendant

  /**
   * @description Set Attempt to set focus on the current node.
   * @param element
   *          The node to attempt to focus on.
   * @returns {boolean}
   *  true if element is focused.
   */
  aria.Utils.attemptFocus = function (element) {
    if (!aria.Utils.isFocusable(element)) {
      return false;
    }

    aria.Utils.IgnoreUtilFocusChanges = true;
    try {
      element.focus();
    } catch (e) {
      // continue regardless of error
    }
    aria.Utils.IgnoreUtilFocusChanges = false;
    return document.activeElement === element;
  }; // end attemptFocus

  /* Modals can open modals. Keep track of them with this array. */
  aria.OpenDialogList = aria.OpenDialogList || new Array(0);

  /**
   * @returns {object} the last opened dialog (the current dialog)
   */
  aria.getCurrentDialog = function () {
    if (aria.OpenDialogList && aria.OpenDialogList.length) {
      return aria.OpenDialogList[aria.OpenDialogList.length - 1];
    }
  };

  aria.closeCurrentDialog = function () {
    var currentDialog = aria.getCurrentDialog();
    if (currentDialog) {
      currentDialog.close(true);
      return true;
    }
    return false;
  };

  aria.handleEscape = function (event) {
    var key = event.which || event.keyCode;

    if (key === aria.KeyCode.ESC) {
      // Se il focus Ã¨ all'interno di un dropdown dopo la chiusura della modale
      const activeElement = document.activeElement;
      if (activeElement && activeElement.closest('.rtds-dropdown-menu__list')) {
        const dropdownMenu = activeElement.closest('.rtds-dropdown-menu');
        if (dropdownMenu) {
          const dropdownList = dropdownMenu.querySelector('.rtds-dropdown-menu__list');
          const dropdownTrigger = dropdownMenu.querySelector('.rtds-dropdown-trigger');
          if (dropdownList && dropdownTrigger) {
            dropdownList.classList.add('rtds-hidden');
            dropdownTrigger.setAttribute('aria-expanded', 'false');
            dropdownTrigger.focus();
            event.stopPropagation();
            return;
          }
        }
      }
      
      // Gestione normale della chiusura della modale
      if (aria.closeCurrentDialog()) {
        event.stopPropagation();
      }
    }
  };

  document.addEventListener('keyup', aria.handleEscape);

  /**
   * @class
   * @description Dialog object providing modal focus management.
   *
   * Assumptions: The element serving as the dialog container is present in the
   * DOM and hidden. The dialog container has role='dialog'.
   * @param dialogId
   *          The ID of the element serving as the dialog container.
   * @param focusAfterClosed
   *          Either the DOM node or the ID of the DOM node to focus when the
   *          dialog closes.
   * @param focusFirst
   *          Optional parameter containing either the DOM node or the ID of the
   *          DOM node to focus when the dialog opens. If not specified, the
   *          first focusable element in the dialog will receive focus.
   */
  aria.Dialog = function (dialogId, focusAfterClosed, focusFirst) {
    this.dialogNode = document.getElementById(dialogId);
    if (this.dialogNode === null) {
      throw new Error('No element found with id="' + dialogId + '".');
    }

    var validRoles = ['dialog', 'alertdialog'];
    var isDialog = (this.dialogNode.getAttribute('role') || '')
      .trim()
      .split(/\s+/g)
      .some(function (token) {
        return validRoles.some(function (role) {
          return token === role;
        });
      });
    if (!isDialog) {
      throw new Error(
        'Dialog() requires a DOM element with ARIA role of dialog or alertdialog.'
      );
    }

    // Wrap in an individual backdrop element if one doesn't exist
    // Native <dialog> elements use the ::backdrop pseudo-element, which
    // works similarly.
    var backdropClass = 'rtds-dialog-backdrop';
    if (this.dialogNode.parentNode.classList.contains(backdropClass)) {
      this.backdropNode = this.dialogNode.parentNode;
    } else {
      this.backdropNode = document.createElement('div');
      this.backdropNode.className = backdropClass;
      this.dialogNode.parentNode.insertBefore(
        this.backdropNode,
        this.dialogNode
      );
      this.backdropNode.appendChild(this.dialogNode);
    }
    this.backdropNode.classList.add('is-active');

    // Disable scroll on the body element
    document.body.classList.add(aria.Utils.dialogOpenClass);

    if (typeof focusAfterClosed === 'string') {
      this.focusAfterClosed = document.getElementById(focusAfterClosed);
    } else if (typeof focusAfterClosed === 'object') {
      this.focusAfterClosed = focusAfterClosed;
    } else {
      throw new Error(
        'the focusAfterClosed parameter is required for the aria.Dialog constructor.'
      );
    }

    if (typeof focusFirst === 'string') {
      this.focusFirst = document.getElementById(focusFirst);
    } else if (typeof focusFirst === 'object') {
      this.focusFirst = focusFirst;
    } else {
      this.focusFirst = null;
    }

    // Bracket the dialog node with two invisible, focusable nodes.
    // While this dialog is open, we use these to make sure that focus never
    // leaves the document even if dialogNode is the first or last node.
    var preDiv = document.createElement('div');
    this.preNode = this.dialogNode.parentNode.insertBefore(
      preDiv,
      this.dialogNode
    );
    this.preNode.tabIndex = 0;
    var postDiv = document.createElement('div');
    this.postNode = this.dialogNode.parentNode.insertBefore(
      postDiv,
      this.dialogNode.nextSibling
    );
    this.postNode.tabIndex = 0;

    // If this modal is opening on top of one that is already open,
    // get rid of the document focus listener of the open dialog.
    if (aria.OpenDialogList.length > 0) {
      aria.getCurrentDialog().removeListeners();
    }

    this.addListeners();
    aria.OpenDialogList.push(this);
    this.dialogNode.className = 'default-dialog'; // make visible

    if (this.focusFirst) {
      this.focusFirst.focus();
    } else {
      aria.Utils.focusFirstDescendant(this.dialogNode);
    }

    this.lastFocus = document.activeElement;
  }; // end Dialog constructor

  //aria.Dialog.prototype.clearDialog = function () {
    // Array.prototype.map.call(
    //   this.dialogNode.querySelectorAll('input'),
    //   function (input) {
    //     input.value = '';
    //   }
    // );
  //};

  /**
   * @description
   *  Hides the current top dialog,
   *  removes listeners of the top dialog,
   *  restore listeners of a parent dialog if one was open under the one that just closed,
   *  and sets focus on the element specified for focusAfterClosed.
   */
  aria.Dialog.prototype.close = function (isKeyboardClose) {
    aria.OpenDialogList.pop();
    this.removeListeners();
    aria.Utils.remove(this.preNode);
    aria.Utils.remove(this.postNode);
    this.dialogNode.className = 'rtds-hidden';
    this.backdropNode.classList.remove('is-active');

    // Gestione speciale per trigger all'interno di dropdown solo se chiuso da tastiera
    if (isKeyboardClose && this.focusAfterClosed && this.focusAfterClosed.closest('.rtds-dropdown-menu__list')) {
      const dropdownMenu = this.focusAfterClosed.closest('.rtds-dropdown-menu');
      if (dropdownMenu) {
        const dropdownList = dropdownMenu.querySelector('.rtds-dropdown-menu__list');
        if (dropdownList) {
          dropdownList.classList.remove('rtds-hidden');
          // Gestione dell'attributo aria-expanded del trigger
          const dropdownTrigger = dropdownMenu.querySelector('.rtds-dropdown-trigger');
          if (dropdownTrigger) {
            dropdownTrigger.setAttribute('aria-expanded', 'true');
          }
        }
      }
    } else if (this.focusAfterClosed && this.focusAfterClosed.closest('.rtds-dropdown-menu__list')) {
      // Se chiuso da mouse, chiudi il dropdown
      const dropdownMenu = this.focusAfterClosed.closest('.rtds-dropdown-menu');
      if (dropdownMenu) {
        const dropdownList = dropdownMenu.querySelector('.rtds-dropdown-menu__list');
        const dropdownTrigger = dropdownMenu.querySelector('.rtds-dropdown-trigger');
        if (dropdownList && dropdownTrigger) {
          dropdownList.classList.add('rtds-hidden');
          dropdownTrigger.setAttribute('aria-expanded', 'false');
        }
      }
    }

    this.focusAfterClosed.focus();

    // If a dialog was open underneath this one, restore its listeners.
    if (aria.OpenDialogList.length > 0) {
      aria.getCurrentDialog().addListeners();
    } else {
      document.body.classList.remove(aria.Utils.dialogOpenClass);
    }
  }; // end close

  /**
   * @description
   *  Hides the current dialog and replaces it with another.
   * @param newDialogId
   *  ID of the dialog that will replace the currently open top dialog.
   * @param newFocusAfterClosed
   *  Optional ID or DOM node specifying where to place focus when the new dialog closes.
   *  If not specified, focus will be placed on the element specified by the dialog being replaced.
   * @param newFocusFirst
   *  Optional ID or DOM node specifying where to place focus in the new dialog when it opens.
   *  If not specified, the first focusable element will receive focus.
   */
  aria.Dialog.prototype.replace = function (
    newDialogId,
    newFocusAfterClosed,
    newFocusFirst
  ) {
    aria.OpenDialogList.pop();
    this.removeListeners();
    aria.Utils.remove(this.preNode);
    aria.Utils.remove(this.postNode);
    this.dialogNode.className = 'rtds-hidden';
    this.backdropNode.classList.remove('is-active');

    var focusAfterClosed = newFocusAfterClosed || this.focusAfterClosed;
    new aria.Dialog(newDialogId, focusAfterClosed, newFocusFirst);
  }; // end replace

  aria.Dialog.prototype.addListeners = function () {
    document.addEventListener('focus', this.trapFocus, true);
  }; // end addListeners

  aria.Dialog.prototype.removeListeners = function () {
    document.removeEventListener('focus', this.trapFocus, true);
  }; // end removeListeners

  aria.Dialog.prototype.trapFocus = function (event) {
    if (aria.Utils.IgnoreUtilFocusChanges) {
      return;
    }
    var currentDialog = aria.getCurrentDialog();
    if (currentDialog.dialogNode.contains(event.target)) {
      currentDialog.lastFocus = event.target;
    } else {
      aria.Utils.focusFirstDescendant(currentDialog.dialogNode);
      if (currentDialog.lastFocus == document.activeElement) {
        aria.Utils.focusLastDescendant(currentDialog.dialogNode);
      }
      currentDialog.lastFocus = document.activeElement;
    }
  }; // end trapFocus

  window.openDialog = function (dialogId, focusAfterClosed, focusFirst) {
    new aria.Dialog(dialogId, focusAfterClosed, focusFirst);
  };

  window.closeDialog = function (closeButton) {
    var topDialog = aria.getCurrentDialog();
    if (topDialog && topDialog.dialogNode.contains(closeButton)) {
      topDialog.close(false);
    }
  }; // end closeDialog

  window.replaceDialog = function (
    newDialogId,
    newFocusAfterClosed,
    newFocusFirst
  ) {
    var topDialog = aria.getCurrentDialog();
    if (topDialog.dialogNode.contains(document.activeElement)) {
      topDialog.replace(newDialogId, newFocusAfterClosed, newFocusFirst);
    }
  }; // end replaceDialog

  // Gestione automatica dei modali con classe rtds-dialog--visible
  document.addEventListener('DOMContentLoaded', function() {
    var visibleDialogs = document.querySelectorAll('.rtds-dialog--visible');
    visibleDialogs.forEach(function(dialog) {
      var dialogElement = dialog.querySelector('[role="dialog"]');
      if (dialogElement) {
        openDialog(dialogElement.id, document.body);
      }
    });
  });

  // Inizializza velocemente solo i toggle nella modale
  window.originalOpenDialog = window.openDialog;
  window.openDialog = function(dialogId, focusAfterClosed, focusFirst) {
    // Chiama la funzione originale
    originalOpenDialog(dialogId, focusAfterClosed, focusFirst);
    
    // Inizializza solo i toggle nella modale
    var dialog = document.getElementById(dialogId);
    if (dialog) {
      var toggleButtons = dialog.querySelectorAll('[data-module="opendata_theme_toggle"]');
      toggleButtons.forEach(function(button) {
        if (!button._toggleInitialized) {
          // Inizializza lo stato corretto del pulsante nella modale
          button.setAttribute('aria-expanded', 'false');
          
          // Nascondi inizialmente gli elementi dopo il 10°
          var targetSelector = button.getAttribute('data-module-target');
          var container = targetSelector ? $(targetSelector) : $(button).closest('.rtds-facets__content');
          if (container.length) {
            var allItems = container.find('ul li');
            allItems.each(function(index) {
              if (index >= 10) {
                this.style.display = 'none';
                $(this).addClass('rtds-hidden');
              }
            });
          }
          $(button).on('click', function(event) {
            event.preventDefault();
            
            var targetSelector = button.getAttribute('data-module-target');
            var container = $(targetSelector);
            var allItems = container.find('.rtds-facets__item');
            
            // SOLO LOGICA MODALE - usa il comando jQuery che funziona
            $(targetSelector + " .rtds-facets__item.rtds-hidden").toggle();
            
            // Toggle etichette
            $(button).find('.rtds-btn__label-show, .rtds-btn__label-hide').toggleClass('rtds-hidden');
          });
          button._toggleInitialized = true;
        }
      });
    }
  };
})();
'use strict';
/**
 * @namespace aria
 */

var aria = aria || {};

/**
 * @description
 *  Key code constants
 */
aria.KeyCode = {
  BACKSPACE: 8,
  TAB: 9,
  RETURN: 13,
  SHIFT: 16,
  ESC: 27,
  SPACE: 32,
  PAGE_UP: 33,
  PAGE_DOWN: 34,
  END: 35,
  HOME: 36,
  LEFT: 37,
  UP: 38,
  RIGHT: 39,
  DOWN: 40,
  DELETE: 46,
};

aria.Utils = aria.Utils || {};

// Polyfill src https://developer.mozilla.org/en-US/docs/Web/API/Element/matches
aria.Utils.matches = function (element, selector) {
  if (!Element.prototype.matches) {
    Element.prototype.matches =
      Element.prototype.matchesSelector ||
      Element.prototype.mozMatchesSelector ||
      Element.prototype.msMatchesSelector ||
      Element.prototype.oMatchesSelector ||
      Element.prototype.webkitMatchesSelector ||
      function (s) {
        var matches = element.parentNode.querySelectorAll(s);
        var i = matches.length;
        while (--i >= 0 && matches.item(i) !== this) {
          // empty
        }
        return i > -1;
      };
  }

  return element.matches(selector);
};

aria.Utils.remove = function (item) {
  if (item.remove && typeof item.remove === 'function') {
    return item.remove();
  }
  if (
    item.parentNode &&
    item.parentNode.removeChild &&
    typeof item.parentNode.removeChild === 'function'
  ) {
    return item.parentNode.removeChild(item);
  }
  return false;
};

aria.Utils.isFocusable = function (element) {
  if (element.tabIndex < 0) {
    return false;
  }

  if (element.disabled) {
    return false;
  }

  switch (element.nodeName) {
    case 'A':
      return !!element.href && element.rel != 'ignore';
    case 'INPUT':
      return element.type != 'hidden';
    case 'BUTTON':
    case 'SELECT':
    case 'TEXTAREA':
      return true;
    default:
      return false;
  }
};

aria.Utils.getAncestorBySelector = function (element, selector) {
  if (!aria.Utils.matches(element, selector + ' ' + element.tagName)) {
    // Element is not inside an element that matches selector
    return null;
  }

  // Move up the DOM tree until a parent matching the selector is found
  var currentNode = element;
  var ancestor = null;
  while (ancestor === null) {
    if (aria.Utils.matches(currentNode.parentNode, selector)) {
      ancestor = currentNode.parentNode;
    } else {
      currentNode = currentNode.parentNode;
    }
  }

  return ancestor;
};

aria.Utils.hasClass = function (element, className) {
  return new RegExp('(\\s|^)' + className + '(\\s|$)').test(element.className);
};

aria.Utils.addClass = function (element, className) {
  if (!aria.Utils.hasClass(element, className)) {
    element.className += ' ' + className;
  }
};

aria.Utils.removeClass = function (element, className) {
  var classRegex = new RegExp('(\\s|^)' + className + '(\\s|$)');
  element.className = element.className.replace(classRegex, ' ').trim();
};

aria.Utils.bindMethods = function (object /* , ...methodNames */) {
  var methodNames = Array.prototype.slice.call(arguments, 1);
  methodNames.forEach(function (method) {
    object[method] = object[method].bind(object);
  });
};
/** Modal dialog END **/


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

ckan.module("opendata_theme_toggle", function ($) {
  return {
      initialize: function () {
          this.el.on("click", this._onClick.bind(this));
      },

      _onClick: function (event) {
          event.preventDefault();
          
          var container = this.options.target ? $(this.options.target) : this.el.closest('.rtds-facets__content');
          if (!container.length) return;
          
          var hiddenItems = container.find('.rtds-facets__item.rtds-hidden');
          var isExpanding = hiddenItems.length > 0;
          
          if (isExpanding) {
              // Mostra tutti gli elementi
              hiddenItems.removeClass('rtds-hidden');
              this.el.attr('aria-expanded', 'true');
          } else {
              // Nascondi elementi dopo il 10°
              container.find('.rtds-facets__item').slice(10).addClass('rtds-hidden');
              this.el.attr('aria-expanded', 'false');
          }
          
          // Toggle etichette
          this.el.find('.rtds-btn__label-show, .rtds-btn__label-hide').toggleClass('rtds-hidden');
      },
  };
});