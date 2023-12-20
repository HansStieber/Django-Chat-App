function validateLoginForm() {
  const username = usernameLogin.value.trim();
  const password = passwordLogin.value.trim();
  loginButton.disabled = !(username && password);
}


function validateRegisterForm() {
  const fn = firstname.value.trim();
  const ln = lastname.value.trim();
  const username = usernameRegister.value.trim();
  const password = passwordRegister.value.trim();
  const passwordRep = passwordRepeat.value.trim();
  registerButton.disabled = !(fn && ln && username && password && passwordRep);
}


function disableSpace(event) {
  if (event.key === " " || event.code === "Space") {
    event.preventDefault();
  }
}


async function sendMessage(chatId) {
  const formData = createFormData();
  const formattedDate = getCurrentDateInRightFormat();
  const username = getAuthorUsername();

  try {
    displayMessage(username, formattedDate);
    await sendChatMessage(chatId, formData);
    confirmMessageSent(username, formattedDate);
    clearMessageField();
  } catch (error) {
    console.error("An error occurred", error);
  }
}


function createFormData() {
  const fd = new FormData();
  const token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  fd.append("textmessage", messageField.value);
  fd.append("csrfmiddlewaretoken", token);
  return fd;
}


function getAuthorUsername() {
  const authorSpan = document.querySelector('.author');
  return authorSpan.dataset.username;
}


function displayMessage(username, formattedDate) {
  messagesContainer.innerHTML += `
    <div class="message-container">
      <div>
        <span class="author">${username}</span><span class="creation-time">${formattedDate}</span>
      </div>
      <div id="newMessage" class="message-text alert-text">
        ${messageField.value}
      </div>
    </div>
  `;
  messagesContainer.lastElementChild.scrollIntoView({ behavior: "smooth" });
}


async function sendChatMessage(chatId, formData) {
  const response = await fetch(`/chat/${chatId}/`, {
    method: "POST",
    body: formData,
  });
}


function confirmMessageSent() {
  newMessage.classList.remove('alert-text');
}


function clearMessageField() {
  messageField.value = null;
}


function getCurrentDateInRightFormat() {
  const currentDate = new Date();
  const options = { month: 'short', day: 'numeric', year: 'numeric' };
  const formattedDate = currentDate.toLocaleDateString('en-US', options);
  return `${formattedDate}`;
}


document.addEventListener('DOMContentLoaded', function() {
  var dialog = document.querySelector('dialog');
  var showDialogButton = document.querySelector('#show-dialog');

  if (dialog && !dialog.showModal) {
    dialogPolyfill.registerDialog(dialog);
  }

  if (dialog) {
    showDialogButton.addEventListener('click', function() {
      dialog.showModal();
    });

    dialog.querySelector('.close').addEventListener('click', function() {
      dialog.close();
    });
  }
});
