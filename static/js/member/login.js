function idchk(id) {
  const id_chk = /^(?=.*[a-zA-Z])[a-zA-Z0-9]{2,10}$/g;
  return id_chk.test(id);
}

function password_chk(pwd) {
  const pwd_chk = /^(?=.*[a-zA-Z])(?=.*[!@#$%~])(?=.*[0-9]).{6,16}/;
  return pwd_chk.test(pwd);
}

function login() {
  const id = document.getElementById("nameInput").value;
  const pwd = document.getElementById("passwordInput").value;
  if (idchk(id)) {
      if (password_chk(pwd) ) {
      let data = {
        'id': id,
        'password': pwd
      }
      $.ajax({
        type: "POST",
        url: "login",
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(data),
        success: function (response) {     
          window.location.href = "/";
        },
      });
    }
    else {
      alert("비밀번호 형식이 올바르지 않습니다.");
    }
  } else {
    alert("아이디 형식이 올바르지 않습니다.");
  }
}