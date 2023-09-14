function idchk(id) {
  const id_chk = /^(?=.*[a-zA-Z])[a-zA-Z0-9]{8,12}$/g;
  return id_chk.test(id);
}

function password_chk(pwd) {
  const pwd_chk = /^(?=.*[a-zA-Z])(?=.*[!@#$%~])(?=.*[0-9]).{8,15}/;
  return pwd_chk.test(pwd);
}

function playsignup() {
  const id = document.getElementById("nameInput").value;
  const pwd = document.getElementById("pwdInput").value;
  const pwdchk = document.getElementById("pwdInput_chk").value;
  const pwd_chkbtn = document.querySelector(".pwdchk_button");
  const signup_btn = document.querySelector(".signup_button");

  if (idchk(id)) {
    if (password_chk(pwd)) {
      if (pwd == pwdchk) {
        pwd_chkbtn.style.display = "none";
        signup_btn.style.display = "inline-block";
      } else {
        alert("비밀번호가 일치하지 않습니다.");
      }
    } else {
      alert("비밀번호 형식이 올바르지 않습니다.");
    }
  } else {
    alert("아이디 형식이 올바르지 않습니다.");
  }
}
