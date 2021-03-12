ask = (question, link) => {
    result = confirm(question);
    if (result) {
        document.location.href = link
    }
}