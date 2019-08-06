function showSearchText() {
  element = document.getElementById('search-phrase');
  field = document.getElementById('search');
  console.log(field.value)
  element.innerHTML = '<h3>' + field.value + '</h3>'
}

