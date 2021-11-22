function regPasswordType(p1) {
  var regex = /^(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*[0-9]).{6,16}/;
  return regex.test(p1);
}

function idchk(p0) {
  var idReg = /^[A-za-z0-9]{5,15}/g;
  return idReg.test(p0);
}

function test() {
  const p0 = document.getElementById("nameInput").value;
  const p1 = document.getElementById("pwdInput").value;
  const p2 = document.getElementById("pwdInput_chk").value;
  const signupbtn = document.querySelector(".signup_btn");
  const signup_btn = document.querySelector(".signup_button");

  if (idchk(p0)) {
    if (regPasswordType(p1)) {
      if (p1 == p2) {
        signupbtn.style.display = "block";
        signup_btn.style.display = "none";
      } else {
        alert("비밀번호가 일치하지 않습니다.");
      }
    } else {
      alert("비밀번호가 정규식에 맞지 않습니다.");
    }
  } else {
    alert("아이디가 정규식에 맞지 않습니다.");
  }
}
