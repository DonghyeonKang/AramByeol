$(document).ready(function () {
    const sessionString = session_check();    // 세션체크 후
	get_daytable(sessionString);     // 데이터 로딩 후
    event_modal();      // 모달 이벤트 처리
});

const session_check = () => {
    let sessionExist;
    $.ajax({
        type: 'POST',
        url: '/api/session_check',
        async: false,
        data: {},
        success: function (response) {
            if(response == '0') {   // 세션 없음
                $("#login").append("<a href=\"/member/login.html\" id=\"login-button\"><img src=\"/static/images/login.png\" alt=\"Login\"></a>");
                sessionExist = 0;
            } else {    // 세션 있음
                $("#login").append("<a id=\"logout-button\"><img src=\"/static/images/logout.png\" alt=\"Login\"></a>");
                sessionExist = 1;
            }
        }
    });

    if (sessionExist == 0) {
        return "<span>";
    } else {
        return "<span class=\"open\">";
    }
}

const logout = () => {
    $.ajax({
        type: 'POST',
        url: '/logout',
        async: true,
        data: {},
        success: function(answer) {
            if(answer == '1'){  //로그아웃 성공시 새로고침
                location.reload();  
            }
        }
    });
}

window.addEventListener('load', function(){
    logoutbutton = document.querySelector("#logout-button");
    logoutbutton.addEventListener('click', () => {
        logout();
    });
});

const get_daytable = (sessionString)  => {
    $.ajax({
		type: 'GET',
		url: '/api/list',
        async: false,
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
            // console.log(days);
            // console.log(morning);
            // console.log(lunch);
            // console.log(dinner);
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
            
            // 메뉴가 없을 때. (해당 날짜가 없을 때)
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
                        morning_info = morning_info  + sessionString + morning[i][2] + "</span></br>";
                    else if(morning[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            morning_info = morning_info + "<p class=\"course\">A</p></br>"
                        }
                        morning_info = morning_info + sessionString + morning[i][2] + "</span></br>";
                    }
                    else if(morning[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            morning_info = morning_info + "<p class=\"course\">B</p></br>"
                        }
                        morning_info = morning_info + sessionString + morning[i][2] + "</span></br>";
                    }
                    else if(morning[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            morning_info = morning_info + "<p class=\"course\">C</p></br>"
                        }
                        morning_info = morning_info + sessionString + morning[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            morning_info = morning_info + "<p class=\"course\">테이크아웃</p></br>"

                        }
                        morning_info = morning_info + sessionString +morning[i][2] + "</span>" + "</br>";
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
                        lunch_info = lunch_info + sessionString + lunch[i][2] + "</span></br>";
                    else if(lunch[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            lunch_info = lunch_info + "<p class=\"course\"> A </p></br>"
                        }
                        lunch_info = lunch_info + sessionString + lunch[i][2] + "</span></br>";
                    }
                    else if(lunch[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            lunch_info = lunch_info + "<p class=\"course\"> B </p></br>"
                        }
                        lunch_info = lunch_info + sessionString + lunch[i][2] + "</span></br>";
                    }
                    else if(lunch[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            lunch_info = lunch_info + "<p class=\"course\"> C </p></br>"
                        }
                        lunch_info = lunch_info + sessionString + lunch[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            lunch_info = lunch_info + "<p class=\"course\"> 테이크아웃 </p></br>"

                        }
                        lunch_info = lunch_info + sessionString + lunch[i][2] + "</span></br>";
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
                        dinner_info = dinner_info + sessionString + dinner[i][2] + "</span></br>";
                    else if(dinner[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            dinner_info = dinner_info + "<p class=\"course\"> A </p></br>"
                        }
                        dinner_info = dinner_info + sessionString + dinner[i][2] + "</span></br>";
                    }
                    else if(dinner[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            dinner_info = dinner_info + "<p class=\"course\"> B </p></br>"
                        }
                        dinner_info = dinner_info + sessionString + dinner[i][2] + "</span></br>";
                    }
                    else if(dinner[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            dinner_info = dinner_info + "<p class=\"course\"> C </p></br>"
                        }
                        dinner_info = dinner_info +sessionString + dinner[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            dinner_info = dinner_info + "<p class=\"course\"> 테이크아웃 </p></br>"

                        }
                        dinner_info = dinner_info + sessionString + dinner[i][2] + "</span></br>";
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
                        morning_info = morning_info + "<span>" + morning[i][2] + "</span></br>";
                    else if(morning[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            morning_info = morning_info + "<p class=\"course\"> A </p></br>"
                        }
                        morning_info = morning_info + "<span>" + morning[i][2] + "</span></br>";
                    }
                    else if(morning[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            morning_info = morning_info + "<p class=\"course\"> B </p></br>"
                        }
                        morning_info = morning_info + "<span>" + morning[i][2] + "</span></br>";
                    }
                    else if(morning[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            morning_info = morning_info + "<p class=\"course\"> C </p></br>"
                        }
                        morning_info = morning_info + "<span>" + morning[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            morning_info = morning_info + "<p class=\"course\"> 테이크아웃 </p></br>"

                        }
                        morning_info = morning_info + "<span>" + morning[i][2] + "</span></br>";
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
                            lunch_info = lunch_info + "<p class=\"course\"> A </p></br>"
                        }
                        lunch_info = lunch_info + "<span>" + lunch[i][2] + "</span></br>";
                    }
                    else if(lunch[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            lunch_info = lunch_info + "<p class=\"course\"> B </p></br>"
                        }
                        lunch_info = lunch_info + "<span>" + lunch[i][2] + "</span></br>";
                    }
                    else if(lunch[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            lunch_info = lunch_info + "<p class=\"course\"> C </p></br>"
                        }
                        lunch_info = lunch_info + "<span>" + lunch[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            lunch_info = lunch_info + "<p class=\"course\"> 테이크아웃 </p></br>"

                        }
                        lunch_info = lunch_info + "<span>" + lunch[i][2] + "</span></br>";
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
                        dinner_info = dinner_info + "<span>" + dinner[i][2] + "</span></br>";
                    else if(dinner[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            dinner_info = dinner_info + "<p class=\"course\"> A </p></br>"
                        }
                        dinner_info = dinner_info + "<span>" + dinner[i][2] + "</span></br>";
                    }
                    else if(dinner[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            dinner_info = dinner_info + "<p class=\"course\"> B </p></br>"
                        }
                        dinner_info = dinner_info + "<span>" + dinner[i][2] + "</span></br>";
                    }
                    else if(dinner[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            dinner_info = dinner_info + "<p class=\"course\"> C </p></br>"
                        }
                        dinner_info = dinner_info + "<span>" + dinner[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            dinner_info = dinner_info + "<p class=\"course\"> 테이크아웃 </p></br>"

                        }
                        dinner_info = dinner_info + "<span>" + dinner[i][2] + "</span></br>";
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
                        morning_info = morning_info + "<span>" + morning[i][2] + "</span></br>";
                    else if(morning[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            morning_info = morning_info + "<p class=\"course\"> A </p></br>"
                        }
                        morning_info = morning_info + "<span>" + morning[i][2] + "</span></br>";
                    }
                    else if(morning[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            morning_info = morning_info + "<p class=\"course\"> B </p></br>"
                        }
                        morning_info = morning_info + "<span>" + morning[i][2] + "</span></br>";
                    }
                    else if(morning[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            morning_info = morning_info + "<p class=\"course\"> C </p></br>"
                        }
                        morning_info = morning_info + "<span>" + morning[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            morning_info = morning_info + "<p class=\"course\"> 테이크아웃 </p></br>"

                        }
                        morning_info = morning_info + "<span>" + morning[i][2] + "</span></br>";
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
                        lunch_info = lunch_info + "<span>" + lunch[i][2] + "</span></br>";
                    else if(lunch[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            lunch_info = lunch_info + "<p class=\"course\"> A </p></br>"
                        }
                        lunch_info = lunch_info + "<span>" + lunch[i][2] + "</span></br>";
                    }
                    else if(lunch[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            lunch_info = lunch_info + "<p class=\"course\"> B </p></br>"
                        }
                        lunch_info = lunch_info + "<span>" + lunch[i][2] + "</span></br>";
                    }
                    else if(lunch[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            lunch_info = lunch_info + "<p class=\"course\"> C </p></br>"
                        }
                        lunch_info = lunch_info + "<span>" + lunch[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            lunch_info = lunch_info + "<p class=\"course\"> 테이크아웃 </p></br>"

                        }
                        lunch_info = lunch_info + "<span>" + lunch[i][2] + "</span></br>";
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
                        dinner_info = dinner_info + "<span>" + dinner[i][2] + "</span></br>";
                    else if(dinner[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            dinner_info = dinner_info + "<p class=\"course\"> A </p></br>"
                        }
                        dinner_info = dinner_info + "<span>" + dinner[i][2] + "</span></br>";
                    }
                    else if(dinner[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            dinner_info = dinner_info + "<p class=\"course\"> B </p></br>"
                        }
                        dinner_info = dinner_info + "<span>" + dinner[i][2] + "</span></br>";
                    }
                    else if(dinner[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            dinner_info = dinner_info + "<p class=\"course\"> C </p></br>"
                        }
                        dinner_info = dinner_info + "<span>" + dinner[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            dinner_info = dinner_info + "<p class=\"course\"> 테이크아웃 </p></br>"

                        }
                        dinner_info = dinner_info + "<span>" + dinner[i][2] + "</span></br>";
                    }
                }
            }
            option = 0;
            dinner_info = dinner_info + '</td>';
            $('#doublenextdinner').append(dinner_info);
         }
    });
    
}

const event_modal = () => {
    const modal = document.querySelector("#modal");
    const open = document.querySelectorAll(".open");
    const close = document.querySelector(".close-btn");
    const submit = document.querySelector(".submit");
    let name = "";
    //Show modal
    for(let i = 0; i < open.length; i++) {
        open[i].addEventListener("click", () => {
            modal.style.opacity=1;
            modal.style.visibility="visible";
            $('.menu-name').empty();
            temp_html = `
            <a>${open[i].innerHTML}</a>                        
            `;           
            $('.menu-name').append(temp_html);
            name = open[i].innerHTML;

            $.ajax({
                type: 'POST',
                url: '/api/menu_score',
                data: {menu_name:name},
                success: function (response) {
                    $('.menu-score').empty();
                    const score = response['score'];
                    for(let i=1; i<=5; i++){
                        if (i<=score)
                            $('.menu-score').append(`★`);
                        else    
                            $('.menu-score').append(`☆`);

                    }
                }
            });
        });
    }
    //Hide modal
    close.addEventListener("click", () => {
        modal.style.opacity=0;
        modal.style.visibility="hidden";
    });
    
    const star = [document.querySelector(".star .no1"), document.querySelector(".star .no2"), document.querySelector(".star .no3"), document.querySelector(".star .no4"), document.querySelector(".star .no5")];
    const score = [0, 0, 0, 0, 0];
    const empty_star = "/static/images/empty_star.png";
    const full_star = "/static/images/full_star.png";
    
    for(let i = 0;i < 5;i++) {
        star[i].addEventListener("click", () => { 
            for(let j = 0; j < 5; j++){
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

    submit.addEventListener("click", () =>{
        modal.style.opacity=0;
        modal.style.visibility="hidden";
        let score_result = 0;
        for(let i = 0; i < score.length; i++){
            score_result += score[i];
        }
        if (score_result > 0){
            $.ajax({
                type: 'POST',
                url: '/api/score',
                data: {menu_name:name, menu_score:score_result},
                success: function (response) {
                    // console.log(name)
                    alert(response['msg'])
                    window.location.reload()
                }
            });
        }
    });
}