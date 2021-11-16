$(document).ready(function () {
	get_daytable();
});

function get_daytable() {
	$.ajax({
		type: 'GET',
		url: '/api/list',
		data: {},
		success: function (response) {
            const date = new Date();
            const day = new Date();
            const tomorrow = new Date(date.setDate(date.getDate() + 1));
            const after_tomorrow = new Date(date.setDate(date.getDate() + 1));

            const todays = day.getFullYear() +'-'+ ('0' + (day.getMonth() + 1)).slice(-2) +'-'+ ('0' + day.getDate()).slice(-2);
            const tomorrows = tomorrow.getFullYear() +'-'+ ('0' + (tomorrow.getMonth() + 1)).slice(-2) +'-'+ ('0' + tomorrow.getDate()).slice(-2);
            const after_tomorrows = after_tomorrow.getFullYear() +'-'+ ('0' + (after_tomorrow.getMonth() + 1)).slice(-2) +'-'+ ('0' + after_tomorrow.getDate()).slice(-2);                
            let this_day;
            let tomorrow_day;
            let after_day;
            
            let days = response['days'];
            let morning = response['morning'];
            let lunch = response['lunch'];
            let dinner = response['dinner'];
            console.log(days);
            console.log(morning);
            console.log(lunch);
            console.log(dinner);
            for (let i = 0; i < days.length; i++){
                if (days[i][1] === todays){
                    this_day = days[i][0];
                }
                if (days[i][1] === tomorrows){
                    tomorrow_day = days[i][0];
                }
                if (days[i][1] === after_tomorrows){
                    after_day = days[i][0];
                }
            }
            
            if(this_day === undefined){
                this_day = "기다리셈";
            }
            if(tomorrow_day === undefined){
                tomorrow_day = "기다리셈";
            }
            if(after_day === undefined){
                after_day = "기다리셈";
            }

            /* 오늘 */
            let morning_info = ""
            let lunch_info = ""
            let dinner_info = ""
            let option = 0;
            morning_info = morning_info + '<td>';
            for(let i = 0; i < morning.length; i++){
                if(this_day === morning[i][0]){
                    if(morning[i][1] === 'none')
                        morning_info = morning_info  + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    else if(morning[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            morning_info = morning_info + " A </br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    }
                    else if(morning[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            morning_info = morning_info + "</br> B </br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    }
                    else if(morning[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            morning_info = morning_info + "</br> C </br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            morning_info = morning_info + "</br> 테이크아웃 </br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" +morning[i][2] + "</span>" + "</br>";
                    }
                }
            }
            option = 0;
            morning_info = morning_info + '</td>';
            morning_info = morning_info + '<td>';
            $('#morning').append(morning_info);

            lunch_info = lunch_info + '<td>';
            for(let i = 0; i < lunch.length; i++){
                if(this_day === lunch[i][0]){
                    if(lunch[i][1] === 'none')
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    else if(lunch[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            lunch_info = lunch_info + " A </br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                    else if(lunch[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            lunch_info = lunch_info + "</br> B </br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                    else if(lunch[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            lunch_info = lunch_info + "</br> C </br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            lunch_info = lunch_info + "</br> 테이크아웃 </br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                }
            }
            option = 0;
            lunch_info = lunch_info + '</td>';
            lunch_info = lunch_info + '<td>';
            $('#lunch').append(lunch_info);

            dinner_info = dinner_info + '<td>';
            for(let i = 0; i < dinner.length; i++){
                if(this_day === dinner[i][0]){
                    if(dinner[i][1] === 'none')
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    else if(dinner[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            dinner_info = dinner_info + "</br> A </br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                    else if(dinner[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            dinner_info = dinner_info + "</br> B </br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                    else if(dinner[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            dinner_info = dinner_info + "</br> C </br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            dinner_info = dinner_info + "</br> 테이크아웃 </br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                }
            }
            option = 0;
            dinner_info = dinner_info + '</td>';
            dinner_info = dinner_info + '<td>';
            $('#dinner').append(dinner_info);

            /* 내일 */
            morning_info = "";
            lunch_info = "";
            dinner_info = "";
            morning_info = morning_info + '<td>';
            for(let i = 0; i < morning.length; i++){
                if(tomorrow_day === morning[i][0]){
                    if(morning[i][1] === 'none')
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    else if(morning[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            morning_info = morning_info + "</br> A </br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    }
                    else if(morning[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            morning_info = morning_info + "</br> B </br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    }
                    else if(morning[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            morning_info = morning_info + "</br> C </br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            morning_info = morning_info + "</br> 테이크아웃 </br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    }
                }
            }
            option = 0;
            morning_info = morning_info + '</td>';
            morning_info = morning_info + '<td>';
            $('#nextmorning').append(morning_info);

            lunch_info = lunch_info + '<td>';
            for(let i = 0; i < lunch.length; i++){
                if(tomorrow_day === lunch[i][0]){
                    if(lunch[i][1] === 'none')
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    else if(lunch[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            lunch_info = lunch_info + "</br> A </br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                    else if(lunch[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            lunch_info = lunch_info + "</br> B </br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                    else if(lunch[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            lunch_info = lunch_info + "</br> C </br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            lunch_info = lunch_info + "</br> 테이크아웃 </br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                }
            }

            option = 0;
            lunch_info = lunch_info + '</td>';
            lunch_info = lunch_info + '<td>';
            $('#nextlunch').append(lunch_info);

            dinner_info = dinner_info + '<td>';
            for(let i = 0; i < dinner.length; i++){
                if(tomorrow_day === dinner[i][0]){
                    if(dinner[i][1] === 'none')
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    else if(dinner[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            dinner_info = dinner_info + "</br> A </br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                    else if(dinner[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            dinner_info = dinner_info + "</br> B </br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                    else if(dinner[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            dinner_info = dinner_info + "</br> C </br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            dinner_info = dinner_info + "</br> 테이크아웃 </br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                }
            }
            option = 0;
            dinner_info = dinner_info + '</td>';
            dinner_info = dinner_info + '<td>';
            $('#nextdinner').append(dinner_info);

            /* 모레 */
            morning_info = "";
            lunch_info = "";
            dinner_info = "";

            morning_info = morning_info + '<td>';
            for(let i = 0; i < morning.length; i++){
                if(after_day === morning[i][0]){
                    if(morning[i][1] === 'none')
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    else if(morning[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            morning_info = morning_info + "</br> A </br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    }
                    else if(morning[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            morning_info = morning_info + "</br> B </br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    }
                    else if(morning[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            morning_info = morning_info + "</br> C </br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            morning_info = morning_info + "</br> 테이크아웃 </br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    }
                }
            }
            option = 0;
            morning_info = morning_info + '</td>';
            $('#doublenextmorning').append(morning_info);

            lunch_info = lunch_info + '<td>';
            for(let i = 0; i < lunch.length; i++){
                if(after_day === lunch[i][0]){
                    if(lunch[i][1] === 'none')
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    else if(lunch[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            lunch_info = lunch_info + "</br> A </br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                    else if(lunch[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            lunch_info = lunch_info + "</br> B </br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                    else if(lunch[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            lunch_info = lunch_info + "</br> C </br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            lunch_info = lunch_info + "</br> 테이크아웃 </br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                }
            }
            option = 0;
            lunch_info = lunch_info + '</td>';
            $('#doublenextlunch').append(lunch_info);
            dinner_info = dinner_info + '<td>';
            for(let i = 0; i < dinner.length; i++){
                if(after_day === dinner[i][0]){
                    if(dinner[i][1] === 'none')
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    else if(dinner[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            dinner_info = dinner_info + "</br> A </br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                    else if(dinner[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            dinner_info = dinner_info + "</br> B </br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                    else if(dinner[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            dinner_info = dinner_info + "</br> C </br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            dinner_info = dinner_info + "</br> 테이크아웃 </br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                }
            }
            option = 0;
            dinner_info = dinner_info + '</td>';
            $('#doublenextdinner').append(dinner_info);
         }
    });
}

window.addEventListener("load", () => {
    const modal = document.querySelector("#modal");
    const open = document.querySelectorAll(".open");
    const close = document.querySelector(".close-btn");
    
    console.log(open);
    //Show modal
    for(let i = 0; i < open.length; i++) {
        open[i].addEventListener("click", () => {
            modal.style.opacity=1;
            modal.style.visibility="visible";
        });
    }
    
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
