console.log("hello");

var searchBar = document.getElementById("search");
var searchForm = document.getElementById("search-form");

searchForm.addEventListener("submit", function(event) {
    event.preventDefault();
})

searchBar.addEventListener("keydown",
    function() {
        console.log(searchBar.value);
    });