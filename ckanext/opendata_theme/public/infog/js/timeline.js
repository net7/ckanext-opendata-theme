
    function loadTimelines(idElement, data, colors) {
        var htmlToAdd = "";
        var descrList = "";
        for (var i = 0; i < data.length; i++) {
            var obj = data[i];
            const idDiv = "timeline" + i;
            const classInvert = i % 2 === 0 ? "" : " invert";
            const classFirst = i === 0 ? " first" : "";
            const classLast = i === data.length - 1 ? " last" : "";
            var currColor = colors[i];
            if (classFirst==="") {
                currColor += ";#" + idDiv +"::before{background-color: " + colors[i-1] + " !important}";
            }
            htmlToAdd += `<div id=` + idDiv + ` class="input` + classInvert + classFirst + classLast + `" style="background-color: ` + currColor + `">
                <span data-year="` + obj.item + `" data-info="` + obj.label + `" data-description="` + obj.description + `" style="background-color: #2e6da4"></span>
                <span class="subspan` + classInvert + `">` + obj.description + `</span>
            </div>`;
            descrList += `<p>` + obj.description + `</p>`;
        }
        var timelineEl = document.getElementById(idElement);
        timelineEl.innerHTML = htmlToAdd;

        const div = document.createElement('div');
        div.className = 'description-flex-container';
        div.innerHTML = descrList;
        timelineEl.parentElement.appendChild(div);

        var inputs = $('.input');
        var paras = $('.description-flex-container').find('p');
        $(inputs).click(function () {
            var t = $(this),
                ind = t.index(),
                matchedPara = $(paras).eq(ind);

            $(t).add(matchedPara).addClass('active');
            $(inputs).not(t).add($(paras).not(matchedPara)).removeClass('active');
        });
    }