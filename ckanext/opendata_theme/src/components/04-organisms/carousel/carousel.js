/* CAROUSEL
* SPLIDE INITIALIZATION
 */
if (document.querySelector('.rtds-carousel')) {
    var splide = new Splide('.rtds-carousel', {
      perPage: 5,
      focus  : 0,
      type: 'loop',
      omitEnd: true,
      perMove: 1,
      gap: '1.5rem',
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
      }
    });
    
    splide.mount();
  }
  