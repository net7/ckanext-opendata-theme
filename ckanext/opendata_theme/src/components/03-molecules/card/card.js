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

const cards = document.querySelectorAll('.rtds-card.is-card-fullclickable');
Array.prototype.forEach.call(cards, card => {
    let down, up, link = card.querySelector('.rtds-card__title a');
    card.style.cursor = 'pointer';
    card.onmousedown = (e) => {
        // Verifica se è il tasto sinistro (0)
        if (e.button === 0) {
            down = +new Date();
        }
    }
    card.onmouseup = (e) => {
        // Procedi solo se è il tasto sinistro (0)
        if (e.button === 0) {
            up = +new Date();
            if ((up - down) < 200) {
                link.click();
            }
        }
    }
});