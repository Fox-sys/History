const search = () => {
    let select = document.body.querySelector('select[name="search_type"]');
    let type = select.options[select.options.selectedIndex].value
    let info = document.body.querySelector('input[class="search"]').value.replace(' ', '-');
    document.location.href = `/?type=${type}&info=${info}`
}