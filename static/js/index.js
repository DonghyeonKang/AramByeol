// 페이지 로딩 시 바로 실행할 함수들
$(document).ready(function () {
	get_daytable(); // 메뉴 테이블을 로딩시켜주는 함수
    event_modal(); // 평가하는 창을 띄우는 함수
});

const get_daytable = ()  => {
    $.ajax({
		type: 'GET',
		url: '/api/list',
        async: false, // 서버와 통신 지연이 생기면 건너 뛰지 않도록 동기 통신하겠다.
		data: {},
		success: function (response) {
            // 오늘 날짜 기준으로 내일 모레 날짜까지 가공
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
            
            // API와 GET 통신
            const days = response['days']; // DB에서 날짜들을 불러옴
            const morning = response['morning'];    // DB에서 아침메뉴를 들고옴
            const lunch = response['lunch'];    // DB에서 점심메뉴를 들고옴
            const dinner = response['dinner'];  // DB에서 저녁메뉴를 들고옴
            // console.log(days);
            // console.log(morning);
            // console.log(lunch);
            // console.log(dinner);
            // DB에서 가져온 날짜와 오늘, 내일, 모레 날짜와 비교하여 같은 날짜만 담기.
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
            
            // 모든 메뉴들과 날짜와 비교하여 오늘, 내일, 모레에 해당하는 메뉴들만 가공
            /* 오늘 */
            let morning_info = ""
            let lunch_info = ""
            let dinner_info = ""
            let option = 0; // 0: A코스, 1: B코스, 2: C코스, 3: 테이크아웃
            morning_info = morning_info + '<td>';
            for(let i = 0; i < morning.length; i++){
                if(this_day === morning[i][0]){
                    if(morning[i][1] === 'none') // open class는 평가창과 연동
                        morning_info = morning_info  + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    else if(morning[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            morning_info = morning_info + "<p class=\"course\">A</p></br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    }
                    else if(morning[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            morning_info = morning_info + "<p class=\"course\">B</p></br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    }
                    else if(morning[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            morning_info = morning_info + "<p class=\"course\">C</p></br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            morning_info = morning_info + "<p class=\"course\">테이크아웃</p></br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" +morning[i][2] + "</span>" + "</br>";
                    }
                }
            }
            option = 0;
            morning_info = morning_info + '</td>';
            morning_info = morning_info + '<td>';
            $('#morning').append(morning_info); // morning id에 붙여넣음.

            lunch_info = lunch_info + '<td>';
            for(let i = 0; i < lunch.length; i++){
                if(this_day === lunch[i][0]){
                    if(lunch[i][1] === 'none')
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    else if(lunch[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            lunch_info = lunch_info + "<p class=\"course\"> A </p></br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                    else if(lunch[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            lunch_info = lunch_info + "<p class=\"course\"> B </p></br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                    else if(lunch[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            lunch_info = lunch_info + "<p class=\"course\"> C </p></br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            lunch_info = lunch_info + "<p class=\"course\"> 테이크아웃 </p></br>"
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
                            dinner_info = dinner_info + "<p class=\"course\"> A </p></br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                    else if(dinner[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            dinner_info = dinner_info + "<p class=\"course\"> B </p></br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                    else if(dinner[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            dinner_info = dinner_info + "<p class=\"course\"> C </p></br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            dinner_info = dinner_info + "<p class=\"course\"> 테이크아웃 </p></br>"
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
                            morning_info = morning_info + "<p class=\"course\"> A </p></br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    }
                    else if(morning[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            morning_info = morning_info + "<p class=\"course\"> B </p></br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    }
                    else if(morning[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            morning_info = morning_info + "<p class=\"course\"> C </p></br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            morning_info = morning_info + "<p class=\"course\"> 테이크아웃 </p></br>"
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
                            lunch_info = lunch_info + "<p class=\"course\"> A </p></br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                    else if(lunch[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            lunch_info = lunch_info + "<p class=\"course\"> B </p></br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                    else if(lunch[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            lunch_info = lunch_info + "<p class=\"course\"> C </p></br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            lunch_info = lunch_info + "<p class=\"course\"> 테이크아웃 </p></br>"
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
                            dinner_info = dinner_info + "<p class=\"course\"> A </p></br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                    else if(dinner[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            dinner_info = dinner_info + "<p class=\"course\"> B </p></br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                    else if(dinner[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            dinner_info = dinner_info + "<p class=\"course\"> C </p></br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            dinner_info = dinner_info + "<p class=\"course\"> 테이크아웃 </p></br>"
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
                            morning_info = morning_info + "<p class=\"course\"> A </p></br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    }
                    else if(morning[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            morning_info = morning_info + "<p class=\"course\"> B </p></br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    }
                    else if(morning[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            morning_info = morning_info + "<p class=\"course\"> C </p></br>"
                        }
                        morning_info = morning_info + "<span class=\"open\">" + morning[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            morning_info = morning_info + "<p class=\"course\"> 테이크아웃 </p></br>"
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
                            lunch_info = lunch_info + "<p class=\"course\"> A </p></br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                    else if(lunch[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            lunch_info = lunch_info + "<p class=\"course\"> B </p></br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                    else if(lunch[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            lunch_info = lunch_info + "<p class=\"course\"> C </p></br>"
                        }
                        lunch_info = lunch_info + "<span class=\"open\">" + lunch[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            lunch_info = lunch_info + "<p class=\"course\"> 테이크아웃 </p></br>"
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
                            dinner_info = dinner_info + "<p class=\"course\"> A </p></br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                    else if(dinner[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            dinner_info = dinner_info + "<p class=\"course\"> B </p></br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                    else if(dinner[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            dinner_info = dinner_info + "<p class=\"course\"> C </p></br>"
                        }
                        dinner_info = dinner_info + "<span class=\"open\">" + dinner[i][2] + "</span></br>";
                    }
                    else{
                        if (option == 3){
                            option = 0;
                            dinner_info = dinner_info + "<p class=\"course\"> 테이크아웃 </p></br>"
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

const event_modal = () => {
    const modal = document.querySelector("#modal"); // 평가창
    const open = document.querySelectorAll(".open"); // 메뉴이름들이 담긴 태그의 클래스 이름은 open
    const close = document.querySelector(".close-btn"); // 평가창의 닫기 버튼
    const submit = document.querySelector(".submit"); // 평가창의 제출버튼
    let name = ""; // 메뉴 이름을 담을거다.
    /* 별점에 관련된 변수들 */
    const star = [document.querySelector(".star .no1"), document.querySelector(".star .no2"), document.querySelector(".star .no3"), document.querySelector(".star .no4"), document.querySelector(".star .no5")];
    const score = [0, 0, 0, 0, 0]; // 평가한 점수
    const empty_star = "static/images/empty_star.png"; // 빈 별
    const full_star = "static/images/full_star.png"; // 꽉찬 별

    //Show modal
    for(let i = 0; i < open.length; i++) {
        open[i].addEventListener("click", () => { // 평가창이 열렸을 때
            modal.style.opacity=1; // 나와랏!
            modal.style.visibility="visible"; // 보일래
            for(let i = 0; i<5; i++){ // 점수 초기화 및 빈 별로 초기화 
                score[i] = 0;
                star[i].src=empty_star;
            }
            $('.menu-name').empty(); // 평가창의 메뉴 나오는 부분을 초기화
            temp_html = `
            <a>${open[i].innerHTML}</a>                        
            `;           
            $('.menu-name').append(temp_html);
            name = open[i].innerHTML; // 평가창에 메뉴이름 띄움

            // DB에서 해당 메뉴의 평균 별점을 불러옴. POST통신
            $.ajax({
                type: 'POST',
                url: '/api/menu_score',
                data: {menu_name:name}, // 평점을 찾을 메뉴이름을 넘겨주고
                success: function (response) {
                    $('.menu-score').empty();
                    const score = response['score']; // DB에서 해당 메뉴의 점수를 리턴.
                    for(let i=1; i<=5; i++){ // 별찍기
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
    close.addEventListener("click", () => { // 닫음 버튼 클릭
        modal.style.opacity=0;  // 이제 안 보일거야..
        modal.style.visibility="hidden";
    });
    
    for(let i = 0;i < 5;i++) {  // 원래는 빈 별인데 누르는 별의 위치에 따라서 꽉찬 별로 채워줌
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

    submit.addEventListener("click", () =>{ // 제출 버튼을 누르면
        modal.style.opacity=0;
        modal.style.visibility="hidden"; // 이제 안보여..
        let score_result = 0; // 별점의 총 합계
        for(let i = 0; i < score.length; i++){
            score_result += score[i];
        }
        if (score_result > 0){ // 0보다 커야함. 별 안누르면 통신안할거야.
            // 서버에 별점 넘길거임. POST 통신
            $.ajax({
                type: 'POST',
                url: '/api/score',
                data: {menu_name:name, menu_score:score_result}, // 메뉴 이름과 점수를 넘겨주고
                success: function (response) {
                    // console.log(name)
                    alert(response['msg'])
                }
            });
        }
    })
    
    
}
