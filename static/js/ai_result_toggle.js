function displayDiv(div, show) {
    if (show) {
        div.style.display = "block";
    }
    else
    {
        div.style.display = "none";
    }
}

function setupToggle(
    visibleRadio,
    hiddenRadio,
    nameDiv,
    posDiv,
    weightDiv,
    existingDiv) {
    displayDiv(nameDiv, visibleRadio.checked)
    displayDiv(posDiv, visibleRadio.checked)
    displayDiv(weightDiv, visibleRadio.checked)
    displayDiv(existingDiv, hiddenRadio.checked)

    hiddenRadio.onchange = function() {
        displayDiv(nameDiv, !hiddenRadio.checked);
        displayDiv(posDiv, !hiddenRadio.checked);
        displayDiv(weightDiv, !hiddenRadio.checked);
        displayDiv(existingDiv, hiddenRadio.checked);
    };
    visibleRadio.onchange = function() {
        displayDiv(nameDiv, visibleRadio.checked);
        displayDiv(posDiv, visibleRadio.checked);
        displayDiv(weightDiv, visibleRadio.checked);
        displayDiv(existingDiv, !visibleRadio.checked);
    };
}

var newEventAreaRadio = document.getElementById('id_event_area_choice_0');
var existingEventAreaRadio = document.getElementById('id_event_area_choice_1');
var newEventAreaName = document.getElementById('div_id_new_event_area_name');
var newEventAreaPosition = document.getElementById('div_id_new_event_area_position');
var newEventAreaWeight = document.getElementById('div_id_new_event_area_weight');
var existingEventAreaList = document.getElementById('div_id_existing_event_area_choice');

setupToggle(
    newEventAreaRadio,
    existingEventAreaRadio,
    newEventAreaName,
    newEventAreaPosition,
    newEventAreaWeight,
    existingEventAreaList
)
