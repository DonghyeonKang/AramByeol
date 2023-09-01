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
  const pwd = document.getElementById("pwdInput").value;

  if (idchk(id)) {
    if (password_chk(pwd) ) {
      $.ajax({
        type: "POST",
        url: "login",
        async: false,
        data: {},
        success: function (response) {     
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