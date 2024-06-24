function displayDiv(div, show) {
    if (show) {
        div.style.display = "block";
    }
    else
    {
        div.style.display = "none";
    }
}

function setupToggle(visibleRadio, hiddenRadio, div) {
    displayDiv(div, visibleRadio.checked)
    hiddenRadio.onchange = function() {
        displayDiv(div, !hiddenRadio.checked);
    };
    visibleRadio.onchange = function() {
        displayDiv(div, visibleRadio.checked);
    };
}

var aiSourceRadio = document.getElementById('id_source_choice_0');
var userSourceRadio = document.getElementById('id_source_choice_1');
var sourceTextDiv = document.getElementById('div_id_source_text')
setupToggle(userSourceRadio, aiSourceRadio, sourceTextDiv)

var aiCountRadio = document.getElementById('id_event_count_choice_0');
var userCountRadio = document.getElementById('id_event_count_choice_1');
var countTextDiv = document.getElementById('div_id_event_count_text')
setupToggle(userCountRadio, aiCountRadio, countTextDiv)

var aiTitleRadio = document.getElementById('id_title_choice_0');
var userTitleRadio = document.getElementById('id_title_choice_1');
var titleTextDiv = document.getElementById('div_id_title_text')
setupToggle(userTitleRadio, aiTitleRadio, titleTextDiv)

var aiDescriptionRadio = document.getElementById('id_description_choice_0');
var userDescriptionRadio = document.getElementById('id_description_choice_1');
var descriptionTextDiv = document.getElementById('div_id_description_text')
setupToggle(userDescriptionRadio, aiDescriptionRadio, descriptionTextDiv)
