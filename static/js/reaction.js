function sendReaction(reactionType, postId) {
  const url = '/reaction/';
  const data = {
    reaction_type: reactionType,
    post_id: postId,
  };

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify(data),
  })
  .then(response => response.json())
  .then(data => {
    const likeCountElement = document.querySelector(`#like-count-${postId}`);
    const dislikeCountElement = document.querySelector(`#dislike-count-${postId}`);
    likeCountElement.innerText = data.like_count;
    dislikeCountElement.innerText = data.dislike_count;
    console.log('Реакция сохранена');
  })
  .catch(error => {
    console.error('Произошла ошибка при сохранении реакции:', error);
  });
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

document.querySelectorAll('[data-reaction-type="like"]').forEach(button => {
  button.addEventListener('click', () => {
    const postId = button.dataset.postId;
    sendReaction('like', postId);
  });
});

document.querySelectorAll('[data-reaction-type="dislike"]').forEach(button => {
  button.addEventListener('click', () => {
    const postId = button.dataset.postId;
    sendReaction('dislike', postId);
  });
});