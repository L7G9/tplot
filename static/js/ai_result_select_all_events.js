function checkAll(checkBoxes, checked){
    for(var i=0; i<checkBoxes.length; i++){
        if(checkBoxes[i].type == 'checkbox')
            checkBoxes[i].checked=checked
    }
}

var selectAllCheckBox = document.getElementById('id_select_all_choice');
var eventCheckBoxes = document.getElementsByName('event_choice')
selectAllCheckBox.onchange = function() {
    checkAll(eventCheckBoxes, selectAllCheckBox.checked);
};
