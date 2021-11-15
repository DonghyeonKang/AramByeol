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

            let temp_html = `<th>${this_day} </br> ${todays}</th>
                    <th>${tomorrow_day} </br> ${tomorrows}</th>
                    <th>${after_day} </br> ${after_tomorrows}</th>`
            $('#week').append(temp_html);
            let morning_info = ""
            let lunch_info = ""
            let dinner_info = ""
            let option = 0;
            morning_info = morning_info + '<td>';
            for(let i = 0; i < morning.length; i++){
                if(this_day === morning[i][0]){
                    if(morning[i][1] === 'none')
                        morning_info = morning_info + morning[i][2] + "</br>";
                    else if(morning[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            morning_info = morning_info + "</br> A </br>"
                        }
                        morning_info = morning_info + morning[i][2] + "</br>";
                    }
                    else if(morning[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            morning_info = morning_info + "</br> B </br>"
                        }
                        morning_info = morning_info + morning[i][2] + "</br>";
                    }
                    else if(morning[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            morning_info = morning_info + "</br> C </br>"
                        }
                        morning_info = morning_info + morning[i][2] + "</br>";
                    }
                    else{
                        if (option == 2){
                            option = 3;
                            morning_info = morning_info + "</br> 테이크아웃 </br>"
                        }
                        morning_info = morning_info + morning[i][2] + "</br>";
                    }
                }
            }
            option = 0;
            morning_info = morning_info + '</td>';
            morning_info = morning_info + '<td>';
            for(let i = 0; i < morning.length; i++){
                if(tomorrow_day === morning[i][0]){
                    if(morning[i][1] === 'none')
                        morning_info = morning_info + morning[i][2] + "</br>";
                    else if(morning[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            morning_info = morning_info + "</br> A </br>"
                        }
                        morning_info = morning_info + morning[i][2] + "</br>";
                    }
                    else if(morning[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            morning_info = morning_info + "</br> B </br>"
                        }
                        morning_info = morning_info + morning[i][2] + "</br>";
                    }
                    else if(morning[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            morning_info = morning_info + "</br> C </br>"
                        }
                        morning_info = morning_info + morning[i][2] + "</br>";
                    }
                    else{
                        if (option == 2){
                            option = 3;
                            morning_info = morning_info + "</br> 테이크아웃 </br>"
                        }
                        morning_info = morning_info + morning[i][2] + "</br>";
                    }
                }
            }
            option = 0;
            morning_info = morning_info + '</td>';
            morning_info = morning_info + '<td>';
            for(let i = 0; i < morning.length; i++){
                if(after_day === morning[i][0]){
                    if(morning[i][1] === 'none')
                        morning_info = morning_info + morning[i][2] + "</br>";
                    else if(morning[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            morning_info = morning_info + "</br> A </br>"
                        }
                        morning_info = morning_info + morning[i][2] + "</br>";
                    }
                    else if(morning[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            morning_info = morning_info + "</br> B </br>"
                        }
                        morning_info = morning_info + morning[i][2] + "</br>";
                    }
                    else if(morning[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            morning_info = morning_info + "</br> C </br>"
                        }
                        morning_info = morning_info + morning[i][2] + "</br>";
                    }
                    else{
                        if (option == 2){
                            option = 3;
                            morning_info = morning_info + "</br> 테이크아웃 </br>"
                        }
                        morning_info = morning_info + morning[i][2] + "</br>";
                    }
                }
            }
            option = 0;
            morning_info = morning_info + '</td>';
            
            $('#morning').append(morning_info);

            lunch_info = lunch_info + '<td>';
            for(let i = 0; i < lunch.length; i++){
                if(this_day === lunch[i][0]){
                    if(lunch[i][1] === 'none')
                        lunch_info = lunch_info + lunch[i][2] + "</br>";
                    else if(lunch[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            lunch_info = lunch_info + "</br> A </br>"
                        }
                        lunch_info = lunch_info + lunch[i][2] + "</br>";
                    }
                    else if(lunch[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            lunch_info = lunch_info + "</br> B </br>"
                        }
                        lunch_info = lunch_info + lunch[i][2] + "</br>";
                    }
                    else if(lunch[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            lunch_info = lunch_info + "</br> C </br>"
                        }
                        lunch_info = lunch_info + lunch[i][2] + "</br>";
                    }
                    else{
                        if (option == 2){
                            option = 3;
                            lunch_info = lunch_info + "</br> 테이크아웃 </br>"
                        }
                        lunch_info = lunch_info + lunch[i][2] + "</br>";
                    }
                }
            }
            option = 0;
            lunch_info = lunch_info + '</td>';
            lunch_info = lunch_info + '<td>';
            for(let i = 0; i < lunch.length; i++){
                if(tomorrow_day === lunch[i][0]){
                    if(lunch[i][1] === 'none')
                        lunch_info = lunch_info + lunch[i][2] + "</br>";
                    else if(lunch[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            lunch_info = lunch_info + "</br> A </br>"
                        }
                        lunch_info = lunch_info + lunch[i][2] + "</br>";
                    }
                    else if(lunch[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            lunch_info = lunch_info + "</br> B </br>"
                        }
                        lunch_info = lunch_info + lunch[i][2] + "</br>";
                    }
                    else if(lunch[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            lunch_info = lunch_info + "</br> C </br>"
                        }
                        lunch_info = lunch_info + lunch[i][2] + "</br>";
                    }
                    else{
                        if (option == 2){
                            option = 3;
                            lunch_info = lunch_info + "</br> 테이크아웃 </br>"
                        }
                        lunch_info = lunch_info + lunch[i][2] + "</br>";
                    }
                }
            }
            option = 0;
            lunch_info = lunch_info + '</td>';
            lunch_info = lunch_info + '<td>';
            for(let i = 0; i < lunch.length; i++){
                if(after_day === lunch[i][0]){
                    if(lunch[i][1] === 'none')
                        lunch_info = lunch_info + lunch[i][2] + "</br>";
                    else if(lunch[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            lunch_info = lunch_info + "</br> A </br>"
                        }
                        lunch_info = lunch_info + lunch[i][2] + "</br>";
                    }
                    else if(lunch[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            lunch_info = lunch_info + "</br> B </br>"
                        }
                        lunch_info = lunch_info + lunch[i][2] + "</br>";
                    }
                    else if(lunch[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            lunch_info = lunch_info + "</br> C </br>"
                        }
                        lunch_info = lunch_info + lunch[i][2] + "</br>";
                    }
                    else{
                        if (option == 2){
                            option = 3;
                            lunch_info = lunch_info + "</br> 테이크아웃 </br>"
                        }
                        lunch_info = lunch_info + lunch[i][2] + "</br>";
                    }
                }
            }
            option = 0;
            lunch_info = lunch_info + '</td>';
            
            $('#lunch').append(lunch_info);

            dinner_info = dinner_info + '<td>';
            for(let i = 0; i < dinner.length; i++){
                if(this_day === dinner[i][0]){
                    if(dinner[i][1] === 'none')
                        dinner_info = dinner_info + dinner[i][2] + "</br>";
                    else if(dinner[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            dinner_info = dinner_info + "</br> A </br>"
                        }
                        dinner_info = dinner_info + dinner[i][2] + "</br>";
                    }
                    else if(dinner[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            dinner_info = dinner_info + "</br> B </br>"
                        }
                        dinner_info = dinner_info + dinner[i][2] + "</br>";
                    }
                    else if(dinner[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            dinner_info = dinner_info + "</br> C </br>"
                        }
                        dinner_info = dinner_info + dinner[i][2] + "</br>";
                    }
                    else{
                        if (option == 2){
                            option = 3;
                            dinner_info = dinner_info + "</br> 테이크아웃 </br>"
                        }
                        dinner_info = dinner_info + dinner[i][2] + "</br>";
                    }
                }
            }
            option = 0;
            dinner_info = dinner_info + '</td>';
            dinner_info = dinner_info + '<td>';
            for(let i = 0; i < dinner.length; i++){
                if(tomorrow_day === dinner[i][0]){
                    if(dinner[i][1] === 'none')
                        dinner_info = dinner_info + dinner[i][2] + "</br>";
                    else if(dinner[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            dinner_info = dinner_info + "</br> A </br>"
                        }
                        dinner_info = dinner_info + dinner[i][2] + "</br>";
                    }
                    else if(dinner[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            dinner_info = dinner_info + "</br> B </br>"
                        }
                        dinner_info = dinner_info + dinner[i][2] + "</br>";
                    }
                    else if(dinner[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            dinner_info = dinner_info + "</br> C </br>"
                        }
                        dinner_info = dinner_info + dinner[i][2] + "</br>";
                    }
                    else{
                        if (option == 2){
                            option = 3;
                            dinner_info = dinner_info + "</br> 테이크아웃 </br>"
                        }
                        dinner_info = dinner_info + dinner[i][2] + "</br>";
                    }
                }
            }
            option = 0;
            dinner_info = dinner_info + '</td>';
            dinner_info = dinner_info + '<td>';
            for(let i = 0; i < dinner.length; i++){
                if(after_day === dinner[i][0]){
                    if(dinner[i][1] === 'none')
                        dinner_info = dinner_info + dinner[i][2] + "</br>";
                    else if(dinner[i][1] === 'A'){
                        if (option == 0){
                            option = 1;
                            dinner_info = dinner_info + "</br> A </br>"
                        }
                        dinner_info = dinner_info + dinner[i][2] + "</br>";
                    }
                    else if(dinner[i][1] === 'B'){
                        if (option == 1){
                            option = 2;
                            dinner_info = dinner_info + "</br> B </br>"
                        }
                        dinner_info = dinner_info + dinner[i][2] + "</br>";
                    }
                    else if(dinner[i][1] === 'C'){
                        if (option == 2){
                            option = 3;
                            dinner_info = dinner_info + "</br> C </br>"
                        }
                        dinner_info = dinner_info + dinner[i][2] + "</br>";
                    }
                    else{
                        if (option == 2){
                            option = 3;
                            dinner_info = dinner_info + "</br> 테이크아웃 </br>"
                        }
                        dinner_info = dinner_info + dinner[i][2] + "</br>";
                    }
                }
            }
            option = 0;
            dinner_info = dinner_info + '</td>';
            
            $('#dinner').append(dinner_info);
         }
    });
}
