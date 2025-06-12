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

function openEditDialog(bookId, bookTitle) {
  let dialog = document.getElementById("editDialog");
  document.getElementById("editBookTitle").value = bookTitle;
  document.getElementById("editForm").action = "/books/" + bookId + "/edit";
  dialog.showModal();
}
