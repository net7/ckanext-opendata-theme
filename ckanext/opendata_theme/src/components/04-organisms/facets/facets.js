/*
 *   This content is licensed according to the W3C Software License at
 *   https://www.w3.org/Consortium/Legal/2015/copyright-software-and-document
 *
 *  From accordion pattern
 */

'use strict';

class FacetToggle {
  constructor(domNode) {
    this.rootEl = domNode;
    this.buttonEl = this.rootEl;

    const controlsId = this.buttonEl.getAttribute('aria-controls');
    this.contentEl = document.getElementById(controlsId);

    this.open = this.buttonEl.getAttribute('aria-expanded') === 'true';

    // add event listeners
    this.buttonEl.addEventListener('click', this.onButtonClick.bind(this));
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
    this.buttonEl.setAttribute('aria-expanded', `${open}`);
    if (open) {
      this.contentEl.removeAttribute('hidden');
    } else {
      this.contentEl.setAttribute('hidden', '');
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
const facetToggles = document.querySelectorAll('button.rtds-facets__toggle');

if (facetToggles && facetToggles.length > 0) {
  facetToggles.forEach((facetToggleEl) => {
    if (facetToggleEl) {
      new FacetToggle(facetToggleEl);
    }
  });
}

/* SHOW MORE BTN */

document.querySelectorAll('.article__show-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    if (btn.getAttribute('data-shown') === 'false') {
      btn.closest('.article').setAttribute('data-expanded', 'true');
      btn.setAttribute('data-shown', 'true');
      btn.textContent = 'Show less';
      btn.closest('.article').querySelector('.article__content').focus();
    } else {
      btn.closest('.article').setAttribute('data-expanded', 'false');
      btn.setAttribute('data-shown', 'false');
      btn.textContent = 'Show more';
    }
  })
})

/* SHOW MORE FACETS */
document.addEventListener('DOMContentLoaded', function() {
  // Seleziona tutti i contenitori che hanno il pulsante "mostra altri"
  const facetsContainers = document.querySelectorAll('.has-show-more');

  // Verifica che esistano contenitori con la classe has-show-more
  if (!facetsContainers || facetsContainers.length === 0) {
    return; // Esci dalla funzione se non ci sono contenitori
  }

  facetsContainers.forEach(container => {
    const showMoreBtn = container.querySelector('.rtds-btn--show-more');
    
    // Verifica che esista il pulsante show more
    if (!showMoreBtn) {
      return; // Salta questo container se non ha il pulsante
    }
    
    const labelShow = showMoreBtn.querySelector('.rtds-btn__label-show');
    const labelHide = showMoreBtn.querySelector('.rtds-btn__label-hide');
    const hiddenItems = container.querySelectorAll('.rtds-facets__item.is-hideable.rtds-hidden');
    
    // Verifica che esistano le etichette
    if (!labelShow || !labelHide) {
      return; // Salta questo container se mancano le etichette
    }
    
    // Inizializza aria-expanded a false
    showMoreBtn.setAttribute('aria-expanded', 'false');

    showMoreBtn.addEventListener('click', () => {
      const isExpanded = showMoreBtn.getAttribute('data-expanded') === 'true';
      
      if (!isExpanded) {
        // Espandi
        hiddenItems.forEach(item => {
          item.classList.remove('rtds-hidden');
        });
        
        // Cambia le etichette
        labelShow.classList.add('rtds-hidden');
        labelHide.classList.remove('rtds-hidden');
        
        // Manda il focus al primo elemento
        if (hiddenItems.length > 0) {
          const firstInput = hiddenItems[0].querySelector('input[type="checkbox"]');
          if (firstInput) {
            firstInput.focus();
          }
        }
        
        showMoreBtn.setAttribute('data-expanded', 'true');
        showMoreBtn.setAttribute('aria-expanded', 'true');
      } else {
        // Collassa
        hiddenItems.forEach(item => {
          item.classList.add('rtds-hidden');
        });
        
        // Ripristina le etichette
        labelShow.classList.remove('rtds-hidden');
        labelHide.classList.add('rtds-hidden');
        
        showMoreBtn.setAttribute('data-expanded', 'false');
        showMoreBtn.setAttribute('aria-expanded', 'false');
      }
    });
  });
});