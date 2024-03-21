function deleteBook(bookId) {
    fetch(`/api/del_books/${bookId}`, {
        method: 'DELETE',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to delete book");  // Throw an error for non-OK responses
        }
        console.log("Book deleted successfully");
        // Optionally, remove the book's row from the table or refresh the page
        location.reload(); // This refreshes the page
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Failed to delete book: " + error.message); // Display the error message
    });
}


// edit button
function editBook(bookId) {
    window.location.href = `/edit-book/${bookId}`;
}



// add book button

// add search function (non functional yet)
function searchBooks() {
    const searchQuery = document.getElementById('searchInput').value.trim();

    if (searchQuery === "") {
        alert("Please enter a search query.");
        return;
    }

    // Make an AJAX request to your backend API
    fetch(`/api/search?query=${encodeURIComponent(searchQuery)}`)
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Failed to fetch search results');
            }
        })
    }
    
//         .then(data => {
//             // Process the retrieved data (e.g., display search results on the page)
//             displaySearchResults(data);
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             alert("Failed to fetch search results. Please try again later.");
//         });
// }

// function displaySearchResults(results) {
//     // Example: assuming 'results' is an array of book objects with id, title, author
//     const searchResultsContainer = document.getElementById('searchResults');
//     searchResultsContainer.innerHTML = ""; // Clear previous search results

//     if (results.length === 0) {
//         searchResultsContainer.innerHTML = "<p>No results found.</p>";
//     } else {
//         const resultList = document.createElement('ul');
//         results.forEach(book => {
//             const listItem = document.createElement('li');
//             listItem.textContent = `${book.title} by ${book.author}`;
//             resultList.appendChild(listItem);
//         });
//         searchResultsContainer.appendChild(resultList);
//     }
