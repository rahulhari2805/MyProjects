document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  // By default, load the inbox
  load_mailbox('inbox');
  
  document.querySelector('#compose-form').onsubmit = send_mail;
  
  

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#full-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#full-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    const html = email.map(user => {
      if (user.read == false) {
        if (mailbox == 'inbox' || mailbox == 'archive') {
          return `<div class="email">
  
          <button id="myemail" onclick="view_mail(${user.id})">From: ${user.sender} &emsp; &emsp; | &emsp; &emsp; Subject: ${user.subject} 
          &emsp; &emsp; &emsp; &emsp; | &emsp; &emsp; &emsp; &emsp; ${user.timestamp}</button>
          
          </div>`;
        }
        else if (mailbox == 'sent') {
          return `<div class="email">
  
          <button id="myemail" onclick="view_sentmail(${user.id})">To: ${user.recipients[0]} &emsp; &emsp; | &emsp; &emsp; Subject: ${user.subject} 
          &emsp; &emsp; &emsp; &emsp; | &emsp; &emsp; &emsp; &emsp; ${user.timestamp}</button>
          
          </div>`;
        }
      }
      else {
        if (mailbox == 'inbox' || mailbox == 'archive') {
          return `<div class="reademail">
  
          <button id="myemail" onclick="view_mail(${user.id})">From: ${user.sender} &emsp; &emsp; | &emsp; &emsp; Subject: ${user.subject} 
          &emsp; &emsp; &emsp; &emsp; | &emsp; &emsp; &emsp; &emsp; ${user.timestamp}</button>
          
          </div>`;
        }
        else if (mailbox == 'sent') {
          return `<div class="email">
  
          <button id="myemail" onclick="view_sentmail(${user.id})">To: ${user.recipients[0]} &emsp; &emsp; | &emsp; &emsp; Subject: ${user.subject} 
          &emsp; &emsp; &emsp; &emsp; | &emsp; &emsp; &emsp; &emsp; ${user.timestamp}</button>
          
          </div>`;
        }
      }
    }).join("");
    
    document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3><p>${html}</p>`;
  });
}

function send_mail() {
  
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients : document.querySelector('#compose-recipients').value,
      subject : document.querySelector('#compose-subject').value,
      body : document.querySelector('#compose-body').value

    })
  })
  .then(response => response.json())
  .then(result => {
    // Print result
    console.log(result);
    load_mailbox('sent');
  });
  return false;
}

function view_mail(email_id) {

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#full-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    
    if (email.archived == false) {
      const data = `<div class="full_email">

                    <div id="archive_button"><button class="btn btn-sm btn-outline-primary" onclick="archive_mail(${email.id})"><b>Archive</b></button></div>
                    <p><b>${email.subject}</b></p><hr>
                    <p id="time">${email.timestamp}</p>
                    <p><b>From :</b> ${email.sender}</p>
                    <p><b>To :</b> ${email.recipients[0]}</p>
                    <hr>
                    <div id="archive_button"><button class="btn btn-sm btn-outline-primary" onclick="reply_mail(${email_id})"><b>Reply</b></button></div>
                    <p><center>${email.body}</center></p>
                    

                    </div>`;
       document.querySelector('#full-view').innerHTML = `${data}`;
      
    }
    else if (email.archived == true) {
      const data = `<div class="full_email">

                    <div id="archive_button"><button class="btn btn-sm btn-outline-primary"  onclick="unarchive_mail(${email.id})"><b>UnArchive</b></button></div>
                    <p><b>${email.subject}</b></p><hr>
                    <p id="time">${email.timestamp}</p>
                    <p><b>From :</b> ${email.sender}</p>
                    <p><b>To :</b> ${email.recipients[0]}</p>
                    <hr>
                    <div id="archive_button"><button class="btn btn-sm btn-outline-primary" onclick="reply_mail(${email_id})"><b>Reply</b></button></div>
                    <p><center>${email.body}</center></p>

                    </div>`;
        document.querySelector('#full-view').innerHTML = `${data}`;
      
    }
  })
  .then(fetch(`/emails/${email_id}`,{
    method :'PUT',
    body : JSON.stringify({
      read: true
    })
  
  }));
}

function view_sentmail(email_id) {

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#full-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    const data = `<div class="full_email">
                  
                  <p><b>${email.subject}</b></p><hr>
                  <p id="time">${email.timestamp}</p>
                  <p><b>From :</b> ${email.sender}</p>
                  <p><b>To :</b> ${email.recipients[0]}</p>
                  <hr>
                  <p><center>${email.body}</center></p>

                  </div>`;
       document.querySelector('#full-view').innerHTML = `${data}`;

  });
}

function archive_mail(email_id) {

  fetch(`/emails/${email_id}`,{
    method :'PUT',
    body : JSON.stringify({
      archived: true
    })
  })
  .then(function() {
    load_mailbox('archive');
  });
}

function unarchive_mail(email_id) {

  fetch(`/emails/${email_id}`,{
    method :'PUT',
    body : JSON.stringify({
      archived: false
    })
  })
  .then(function() {
    load_mailbox('inbox');
  });
}

function reply_mail(email_id) {
  
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#full-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    console.log(email);
    
    document.querySelector('#compose-recipients').value = `${email.sender}`;
    document.querySelector('#compose-body').value = `"On ${email.timestamp} ${email.sender} wrote:" ${email.body}`;
    if (email.subject.charAt(0) == 'R' && email.subject.charAt(1) == 'e') {
      
      document.querySelector('#compose-subject').value = `${email.subject}`;

    }
    else{
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    }
  });
}