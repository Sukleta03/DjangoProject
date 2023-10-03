document.addEventListener('DOMContentLoaded', function() {
  var addTagButton = document.querySelector('.add-tag-button');
  var tagContainer = document.querySelector('.tag-container');

  addTagButton.addEventListener('click', function() {
    var newTag = document.createElement('span');
    newTag.classList.add('edit-tag');
    var newTagInput = document.createElement('input');
    newTagInput.type = 'text';
    newTagInput.name = 'tags';
    newTag.appendChild(newTagInput);
    tagContainer.appendChild(newTag);
    newTagInput.focus();
  });
});