function key_press(event) {
    if (event.key === 'Enter') {
        search();
    }
}

function search() {
    const searchQuery = document.getElementById('search').value.trim();
    if (searchQuery === "") {
        alert("Please enter a search query.");
        return;
    }
    fetch(`/api/search_book_title/${encodeURIComponent(searchQuery)}`)
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Failed to fetch search results');
            }
        })
    }