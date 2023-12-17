function validateLoginForm() {
  const username = usernameLogin.value.trim();
  const password = passwordLogin.value.trim();

  if (username && password) {
    loginButton.removeAttribute("disabled");
  } else {
    loginButton.setAttribute("disabled", "true");
  }
}


function validateRegisterForm() {
  const fn = firstname.value.trim();
  const ln = lastname.value.trim();
  const username = usernameRegister.value.trim();
  const password = passwordRegister.value.trim();
  const passwordRep = passwordRepeat.value.trim();

  if (fn && ln && username && password && passwordRep) {
    registerButton.removeAttribute("disabled");
  } else {
    registerButton.setAttribute("disabled", "true");
  }
}


function disableSpace(event) {
  if (event.key === " " || event.code === "Space") {
    event.preventDefault();
  }
}


async function sendMessage() {
  let fd = new FormData();
  let token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  fd.append("textmessage", messageField.value);
  fd.append("csrfmiddlewaretoken", token);

  let formattedDate = getCurrentDateInRightFormat();

  let authorSpan = document.querySelector('.author');
  let username = authorSpan.dataset.username;

  try {
    messagesContainer.innerHTML += `
      <div class="message-container" id="deleteMessage">
        <div>
          <span class="author">${username}</span><span class="creation-time">${formattedDate}</span>
        </div>
        <div class="message-text alert-text">
          ${messageField.value}
        </div>
      </div>
      `;

    messagesContainer.lastElementChild.scrollIntoView({ behavior: "smooth" });

    let response = await fetch("/chat/", {
      method: "POST",
      body: fd,
    });

    let json = await response.json();
    console.log("json is", json);

    deleteMessage.remove();
    messagesContainer.innerHTML += `
      <div class="message-container">
        <div>
          <span class="author">${username}</span><span class="creation-time">${formattedDate}</span>
        </div>
        <div class="message-text">
          ${messageField.value}
        </div>
      </div>
      `;

    messageField.value = null;
  } catch (e) {
    console.error("An error occurred", e);
  }
}

function getCurrentDateInRightFormat() {
  const months = [
    "Jan.",
    "Feb.",
    "Mar.",
    "Apr.",
    "May",
    "Jun.",
    "Jul.",
    "Aug.",
    "Sep.",
    "Oct.",
    "Nov.",
    "Dec.",
  ];

  const currentDate = new Date();
  const day = currentDate.getDate();
  const month = months[currentDate.getMonth()];
  const year = currentDate.getFullYear();

  const formattedDate = `[${month} ${day}, ${year}]`;
  return formattedDate;
}
