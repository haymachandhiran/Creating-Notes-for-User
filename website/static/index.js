function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}


function generateOTP(){
mob_mail = document.getElementById('mob_mail').value;
if (mob_mail == ""){
alert('Please enter mail id or mobile number to generate OTP');
console.log(mob_mail);
}
else{
fetch("/generate_otp", {
   method: "POST",
    body: JSON.stringify({ mob_mail: mob_mail }),
  })
.then((_res) => (_res).json())
.then((_res) =>{
    var dataReply = _res;
    if (JSON.stringify(dataReply) === '{}')
       {
       console.log('success');
       window.location.href = "/login";
        }
    else
        {
        console.log(dataReply);
        window.location.href = "/sign-up";
        };

});
}
}


function ForgetPassword(){
mob_mail = document.getElementById('mob_mail').value;
if (mob_mail == ""){
alert('Please enter mail id or mobile number to change password');
console.log(mob_mail);
}
else{
fetch("/generate_otp", {
   method: "POST",
    body: JSON.stringify({ mob_mail: mob_mail }),
  })
.then((_res) => (_res).json())
.then((_res) =>{
    var dataReply = _res;
    if (JSON.stringify(dataReply) === '{}')
       {
       window.location.href = "/forget_password";
       console.log('success');
       console.log(json);
        }
    else
        {
        window.location.href = "/sign-up";
        console.log(dataReply);
        console.log(dataReply.error);
        };

});
}
}