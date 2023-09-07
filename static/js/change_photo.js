const uploadButton = document.getElementById('upload-button');
const avatarInput = document.getElementById('avatar-input');

uploadButton.addEventListener('click', () => {
  avatarInput.click();
});

avatarInput.addEventListener('change', () => {
  const form = document.getElementById('avatar-form');
  form.submit();
});
