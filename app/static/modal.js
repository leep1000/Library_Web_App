function openDialog(bookId, bookTitle) {
  let dialog = document.getElementById("deleteDialog");
  document.getElementById("deleteMsg").textContent =
    "Are you sure you want to delete '" + bookTitle + "'?";
  document.getElementById("deleteForm").action = "/books/" + bookId + "/delete";
  dialog.showModal();
}

function closeDialog() {
  document.getElementById("deleteDialog").close();
}

function openEditDialog(bookId, bookTitle, bookAuthor, bookYear, bookIsbn) {
  let dialog = document.getElementById("editDialog");
  document.getElementById("editBookTitle").value = bookTitle;
  document.getElementById("editBookAuthor").value = bookAuthor;
  document.getElementById("editBookYear").value = bookYear;
  document.getElementById("editBookIsbn").value = bookIsbn;
  document.getElementById("editForm").action = "/books/" + bookId + "/edit";
  dialog.showModal();
}

function closeEditDialog() {
  document.getElementById("editDialog").close();
}

function openAddDialog() {
  let dialog = document.getElementById("addDialog");
  document.getElementById("bookTitle").value = "";
  document.getElementById("bookAuthor").value = "";
  document.getElementById("bookYear").value = "";
  document.getElementById("bookIsbn").value = "";
  dialog.showModal();
}

function closeAddDialog() {
  document.getElementById("addDialog").close();
}
