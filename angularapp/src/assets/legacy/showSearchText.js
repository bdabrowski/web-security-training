function showSearchText() {
  element = document.getElementById('search-phrase');
  field = document.getElementById('search');
  element.innerHTML = '<h3>' + field.value + '</h3>'
}
