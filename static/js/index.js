window.addEventListener("load", () => {
  const modal = document.querySelector("#modal");
  const open = document.querySelector(".open");
  const close = document.querySelector(".close-btn");

  //Show modal
  open.addEventListener("click", () => {
    modal.style.opacity=1;
    modal.style.visibility="visible";
  });

  //Hide modal
  close.addEventListener("click", () => {
    modal.style.opacity=0;
    modal.style.visibility="hidden";
  });

  const star = [document.querySelector(".star .no1"), document.querySelector(".star .no2"), document.querySelector(".star .no3"), document.querySelector(".star .no4"), document.querySelector(".star .no5")];
  const score = [0, 0, 0, 0, 0];
  const empty_star = "static/images/empty_star.png";
  const full_star = "static/images/full_star.png";

  for(let i = 0;i < 5;i++) {
    star[i].addEventListener("click", () => { 
      for(let j = 0; j < 5; j++){
        console.log(1);
        if(j <= i && score[j] == 0) {
          star[j].src=full_star;
          score[j] = 1;
        }
        if(j > i && score[j] == 1) {
          star[j].src=empty_star;
          score[j] = 0;
        }
      }
    });
  }
});
