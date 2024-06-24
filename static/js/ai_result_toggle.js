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
    option1Radio,
    option2Radio,
    nameDiv,
    positionDiv,
    weightDiv,
    existingDiv,
) {
    displayDiv(nameDiv, option1Radio.checked)
    displayDiv(positionDiv, option1Radio.checked)
    displayDiv(weightDiv, option1Radio.checked)
    displayDiv(existingDiv, option2Radio.checked)

    option1Radio.onchange = function() {
        displayDiv(nameDiv, option1Radio.checked)
        displayDiv(positionDiv, option1Radio.checked)
        displayDiv(weightDiv, option1Radio.checked)
        displayDiv(existingDiv, !option1Radio.checked)
    };
    option2Radio.onchange = function() {
        displayDiv(nameDiv, !option2Radio.checked)
        displayDiv(positionDiv, !option2Radio.checked)
        displayDiv(weightDiv, !option2Radio.checked)
        displayDiv(existingDiv, option2Radio.checked)
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
    newEventAreaName, newEventAreaPosition, newEventAreaWeight,
    existingEventAreaList,
)
