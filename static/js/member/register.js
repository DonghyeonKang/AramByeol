function test() {
  const p1 = document.getElementById("pwdInput").value;
  const p2 = document.getElementById("pwdInput_chk").value;
  const signupbtn = document.querySelector(".signup_btn");
  if (p1 == p2) {
    signupbtn.style.display = "block";
  } else {
    function deleteBoard(seq) {
      Swal.fire({
        title: "글을 삭제하시겠습니까???",
        text: "삭제하시면 다시 복구시킬 수 없습니다.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "삭제",
        cancelButtonText: "취소",
      }).then((result) => {
        if (result.value) {
          //"삭제" 버튼을 눌렀을 때 작업할 내용을 이곳에 넣어주면 된다.
        }
      });
    }
  }
}
