/* HEADER SCRIPT - mobile management */
document.addEventListener('DOMContentLoaded', function () {
    'use strict';
    if (document.querySelector('.rtds-header')) {
        /* GLOBAL VARIABLES */
        var rootElement = document.documentElement;
        var siteHeader = document.querySelector('.rtds-header');
        var mainHeading = document.querySelector('.rtds-main-heading');
        // var breadcrumb = document.querySelector('.rtds-breadcrumb');
        var headerHeight;
        // var breadcrumbHeight;

        var mainMenuWrapper = document.getElementById('mainNavPanel');
        var headerLinkRight = document.querySelector('.rtds-header-link-right');
        var headerSocialLinks = document.querySelector('.rtds-social-links');
        var headerSecondaryNav = document.querySelector('.rtds-top-bar__navigation');
        var mobilePanelLastEl = document.querySelector('.is-last-element');
        var headerMainActions = document.querySelector('.rtds-main-heading__actions');

        var SiteMenuWrapper = document.getElementById('siteNavWrapper');

        var mobilePanelSecondLastEl = document.querySelector('.is-second-last');

        /* FUNCTIONS */

        function toggleIcon(icon) {
            if (icon.classList.contains('is-hidden')) {
                icon.classList.remove('is-hidden');
                icon.classList.add('is-visible');
            } else if (icon.classList.contains('is-visible')) {
                icon.classList.remove('is-visible');
                icon.classList.add('is-hidden');
            }
        }

        function calculateSiteHeader(header) {
            headerHeight = header.offsetHeight;
            rootElement.style.setProperty('--header-offset', headerHeight + 'px');
        }

        // function calculateBreadcrumbHeader(breadcrumb) {
        //     breadcrumbHeight = breadcrumb.offsetHeight;
        //     rootElement.style.setProperty('--breadcrumb-height', breadcrumbHeight + 'px');
        // }

        function ariaExpandedToggle(target) {
            if (target.getAttribute('aria-expanded') === "false") {
                target.setAttribute('aria-expanded', 'true');
            } else {
                target.setAttribute('aria-expanded', 'false');
            }
        }

        function openOffCanvasMenu(button, targetMenu) {
            button.classList.toggle('is-selected');
            ariaExpandedToggle(button);
            targetMenu.classList.toggle('is-open');
            document.body.classList.toggle('rtds-overflow-hidden');
        }

        function closeMobileMenu() {
            if (document.body.classList.contains('rtds-overflow-hidden')) {
                document.body.classList.remove('rtds-overflow-hidden');
            }

            mainMenuWrapper.classList.remove('is-open');
            document.getElementById('mobileNavToggle').setAttribute('aria-expanded', 'false');
            document.getElementById('mobileNavToggle').classList.remove('is-selected');
        }


        function wrapAndAppend(wrapperClass, elementToWrap, parentElement) {
            // Controlla se l'elemento da avvolgere è già contenuto in un wrapperDiv con la stessa classe
            var existingWrapper = elementToWrap.closest('.' + wrapperClass);

            // Se l'elemento è già avvolto, utilizza il wrapper esistente anziché crearne uno nuovo
            if (existingWrapper) {
                existingWrapper.appendChild(elementToWrap);
            } else {
                // Altrimenti, crea un nuovo wrapperDiv
                var wrapperDiv = document.createElement('div');
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
            if (elementToUnwrap && elementToUnwrap.parentNode === parentElement) {
                parentElement.removeChild(elementToUnwrap);
            }

            if (wrapperDiv && wrapperDiv.parentNode === parentElement) {
                parentElement.removeChild(wrapperDiv);
            }
        }
        function handleResize() {
            if (window.matchMedia("screen and (max-width: 1023px)").matches) {
        
                var topBar = document.querySelector('.rtds-top-bar');
                var bottomBar = document.querySelector('.rtds-bottom-bar');
        
                /* FOR HEADER WITH NAVIGATION IN TOP BAR */
                if (topBar && topBar.contains(SiteMenuWrapper)) {
                    document.querySelector('.rtds-main-heading__container').append(SiteMenuWrapper);
                }
        
                /* FOR HEADER WITH NAVIGATION IN BOTTOM BAR */
                if (bottomBar && bottomBar.contains(SiteMenuWrapper)) {
                    document.querySelector('.rtds-main-heading__container').append(SiteMenuWrapper);
                }
        
                // Verifica altri elementi e le azioni che devono essere fatte su di essi
                if (headerLinkRight) {
                    wrapAndAppend('rtds-primary-navigation__module', headerLinkRight, mainMenuWrapper);
                }
        
                if (headerSecondaryNav) {
                    wrapAndAppend('rtds-primary-navigation__module', headerSecondaryNav, mainMenuWrapper);
                }
        
                if (headerMainActions) {
                    wrapAndAppend('rtds-primary-navigation__module', headerMainActions, mainMenuWrapper);
                }
        
                if (mobilePanelSecondLastEl) {
                    wrapAndAppend('rtds-primary-navigation__module', mobilePanelSecondLastEl, mainMenuWrapper);
                }
        
                if (headerSocialLinks) {
                    wrapAndAppend('rtds-primary-navigation__module', headerSocialLinks, mainMenuWrapper);
                }
        
                calculateSiteHeader(mainHeading);
        
            } else if (window.matchMedia("screen and (min-width: 1024px)").matches) {
                // Se la viewport è maggiore o uguale a 1024px
                var emptyNavModules = document.querySelectorAll('.rtds-primary-navigation__module:not(.is-main):empty');
        
                emptyNavModules.forEach(function (emptyNavModule) {
                    if (SiteMenuWrapper.classList.contains('is-top-nav-positioned')) {
                        var topBarContainer = document.querySelector('.rtds-top-bar__container');
                        if (topBarContainer) {
                            topBarContainer.prepend(SiteMenuWrapper);
                        }
                    }
        
                    if (SiteMenuWrapper.classList.contains('is-bottom-nav-positioned')) {
                        var bottomBarContainer = document.querySelector('.rtds-bottom-bar__container');
                        if (bottomBarContainer) {
                            bottomBarContainer.prepend(SiteMenuWrapper);
                        }
                    }
        
                    if (headerSecondaryNav) {
                        unwrapAndRemove(emptyNavModule, headerSecondaryNav, mainMenuWrapper);
                    }
        
                    if (headerMainActions) {
                        unwrapAndRemove(emptyNavModule, headerMainActions, mainMenuWrapper);
                    }
        
                    if (mobilePanelSecondLastEl) {
                        unwrapAndRemove(emptyNavModule, mobilePanelSecondLastEl, mainMenuWrapper);
                    }
        
                    if (headerSocialLinks) {
                        unwrapAndRemove(emptyNavModule, headerSocialLinks, mainMenuWrapper);
                    }
        
                    if (headerLinkRight) {
                        unwrapAndRemove(emptyNavModule, headerLinkRight, mainMenuWrapper);
                    }
                });
        
                // Riporto headerSocialLinks nel suo posto originale
                if (headerSecondaryNav) {
                    var topBarContainer = document.querySelector('.rtds-top-bar__container');
                    if (topBarContainer) {
                        topBarContainer.prepend(headerSecondaryNav);
                    }
                }
        
                if (headerSocialLinks) {
                    var utilitiesArea = document.querySelector('.rtds-top-bar__utilities-area');
                    if (utilitiesArea) {
                        utilitiesArea.prepend(headerSocialLinks);
                    }
                }
        
                if (headerLinkRight) {
                    var utilitiesArea = document.querySelector('.rtds-top-bar__utilities-area');
                    if (utilitiesArea) {
                        utilitiesArea.prepend(headerLinkRight);
                    }
                }
        
                if (headerMainActions) {
                    document.querySelector('.rtds-main-heading__container').append(headerMainActions);
                }
        
                if (mobilePanelSecondLastEl) {
                    document.querySelector('#siteHeader').append(mobilePanelSecondLastEl);
                }
        
                calculateSiteHeader(siteHeader);
            }
        }
        

        window.addEventListener('resize', handleResize);
        handleResize(); // Initialize on page load

        document.getElementById('mobileNavToggle').addEventListener('click', function (e) {
            e.preventDefault();
            openOffCanvasMenu(this, mainMenuWrapper);
            // console.log('clicked');
        });

        document.addEventListener('keyup', function (e) {
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
                if (mainMenuWrapper.classList.contains('is-open')) {
                    // Verifica se il focus è all'interno del menu principale
                    const isFocusInsideMainMenu = SiteMenuWrapper.contains(document.activeElement) &&
                        !document.activeElement.closest('.rtds-dropdown-menu__item');

                    if (isFocusInsideMainMenu) {
                        closeMobileMenu();

                        // Se disponibile, ripristina il focus sull'elemento principale di apertura menu
                        if (document.getElementById('mobileNavToggle')) {
                            document.getElementById('mobileNavToggle').focus();
                        }
                    }
                }
            }

            // if ((e.key === 'Tab' || e.keyCode === 9) && !mainMenuWrapper.contains(e.target)) {
            //     closeMobileMenu();
            // }
        });

        document.body.addEventListener('click', function (e) {
            if ((!SiteMenuWrapper.contains(e.target) || document.querySelector('.rtds-primary-navigation__backdrop').contains(e.target)) && mainMenuWrapper.classList.contains('is-open')) {
                closeMobileMenu();
            }
        });

    }
});


/* SEARCH DIALOG */
const openModal = () => {
    const modal = document.getElementById('searchModal');
    const modalContent = modal.querySelector('.rtds-modal-content');
    const header = document.querySelector('.rtds-header');

    modal.style.display = 'flex';
    modal.classList.add("rtds-z-20");
    modal.setAttribute('aria-hidden', 'false');
    header.classList.add('has-search-modal-open');

    // Get all the focusable elements inside the modal content
    const focusableElements = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
    const firstFocusable = modalContent.querySelectorAll(focusableElements)[0];
    const fallbackFocusable = modalContent.querySelector('.is-focusable-element'); // Adjust the selector if necessary

    // If there's a focusable element, focus on it; otherwise, focus on the fallback element
    if (firstFocusable) {
        firstFocusable.focus();
    } else if (fallbackFocusable) {
        fallbackFocusable.setAttribute('tabindex', '-1');
        fallbackFocusable.focus();
    }

    if (!document.body.classList.contains('rtds-overflow-hidden')) {
        document.body.classList.add('rtds-overflow-hidden');
    }
};

const closeModal = () => {
    const modal = document.getElementById('searchModal');
    const modalContent = modal.querySelector('.rtds-modal-content');
    const previouslyFocusedElement = document.getElementById('searchModalTrigger');
    const header = document.querySelector('.rtds-header');

    // Remove tabindex from the fallback focusable element
    const fallbackFocusable = modalContent.querySelector('.is-focusable-element');
    if (fallbackFocusable) {
        fallbackFocusable.removeAttribute('tabindex');
    }

    if (document.body.classList.contains('rtds-overflow-hidden')) {
        document.body.classList.remove('rtds-overflow-hidden');
    }

    modal.style.display = 'none';
    modal.setAttribute('aria-hidden', 'true');
    modal.classList.remove("rtds-z-10");
    header.classList.remove('has-search-modal-open');
    previouslyFocusedElement.focus();
};

if (document.getElementById('searchModal')) {
    document.getElementById('searchModalTrigger').addEventListener('click', openModal);

    document.getElementById('closeModal').addEventListener('click', closeModal);

    document.getElementById('searchModal').addEventListener('keydown', function (event) {
        const modalContent = document.querySelector('.rtds-modal-content');
        const focusableElements = modalContent.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
        const firstFocusableElement = focusableElements[0];
        const lastFocusableElement = focusableElements[focusableElements.length - 1];

        if (event.key === 'Tab') {
            if (event.shiftKey && document.activeElement === firstFocusableElement) {
                lastFocusableElement.focus();
                event.preventDefault();
            } else if (!event.shiftKey && document.activeElement === lastFocusableElement) {
                firstFocusableElement.focus();
                event.preventDefault();
            }
        }

        if (event.key === 'Escape') {
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