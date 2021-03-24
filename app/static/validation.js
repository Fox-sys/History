const get_form_elements = () => {
    return document.querySelectorAll('.form_input');
}

const change_field_visibility = (checkbox, field, elements) => {
    let state = elements[checkbox];
    let input = elements[field].parentNode;
    console.log(elements[field])
    if (state.checked) {
        input.style.display = 'none';
    }
    else {
        input.style.display = 'block';
    }
}

const common_validation = (ignore_list=[]) => {
    let elements = get_form_elements();
    let item = null
    for (j = 0; j < elements.length; j++) {
        item = elements[j] 
        if (item.value.length == 0 && ignore_list.indexOf(j) == -1) {
            return false;
        }
    }
    return true;
}

const password_validation = () => {
    let password1 = document.querySelector('input[name="password1"]');
    let password2 = document.querySelector('input[name="password2"]');
    return password1.value === password2.value;
}

const hidden_fields_validation = (checkbox, field, elements) => {
    if (!elements[checkbox].checked && elements[field].value.length == 0){
        return false;
    }
    return true
}   

const profile_edit_validation = () => {
    let ignore_list = [4, 5, 6, 7];
    let elements = get_form_elements()
    change_field_visibility(5, 4, elements)
    change_field_visibility(7, 6, elements)
    return common_validation(ignore_list) && hidden_fields_validation(5, 4, elements) && hidden_fields_validation(7, 6, elements)
}

const solder_validation = () => {
    let elements = get_form_elements();
    let ignore_list = [4, 7];
    change_field_visibility(4, 7, elements)
    return common_validation(ignore_list) && hidden_fields_validation(4, 7, elements);
}

const register_validation = () => {
    return common_validation() && password_validation()
}

const validatiors = {
    "/solders/create/": solder_validation,
    "/login/": common_validation,
    "/register/": register_validation,
    "/profiles/edit/": profile_edit_validation,
    "/changepassword/": common_validation
}

const show_button = () => {
    let button = document.querySelector('.submit_button');
    if (validatiors[document.location.pathname]()) {
        button.style.display = 'block';
    }
    else {
        button.style.display = 'none';
    }
}

window.onload = () => {
    setTimeout(show_button, 1000);
}