function get_value() {
  var a = document.getElementsByClassName("entry-value");
  var listval = [];
  for (let i = 0; i < a.length; i++) {
    listval.push(a[i].value);
  }
  return listval;
}
function convert_string(valueList) {
  var string = "?";
  for (let i = 0; i < valueList.length; i++) {
    string += `v${i}=${valueList[i]}`;
    if (i != (valueList.length - 1)) {
      string += "&";
    }
  }
  return string;
}
function get_values() {
  console.log(convert_string(get_value()));
}
function remove_blur() {
  let body = document.getElementsByClassName("main-body")[0];
  body.classList.remove("blurred");
}
function enable_click() {
  let clickable = document.getElementsByClassName("main-body")[0];
  clickable.style.pointerEvents = "initial";
}
function remove_loader() {
  let loader = document.getElementsByClassName("loader-div")[0];
  loader.remove();
}
var top_section_offset = document.getElementsByClassName("navigation-section")[0].offsetTop;
function fix_top_section() {
  let navigation = document.getElementsByClassName("top-section")[0];
  if (window.scrollY > top_section_offset) {
    navigation.classList.add("top_fixed");
    navigation.classList.add("obscure_top");
  }
  else {
    navigation.classList.remove("top_fixed");
    navigation.classList.remove("obscure_top");
  }
}
document.addEventListener("scroll", fix_top_section);
document.addEventListener("DOMContentLoaded", () => {
  setTimeout(() => {  remove_loader();  enable_click();  remove_blur();  }, 1000);
})
