// 이 페이지가 전송될 때의 state code를 요청
fetch('#').then(function(response){
    const error_code = response['status'];
    let content="";
    // 에러코드가 없거나 200(정상)이 아닐 때
    if(document.createTextNode && error_code != undefined && error_code != 200){
        if (error_code === 404)
            content = " NOT FOUND!";
        else if (error_code === 500)
            content = " INTERNAL ERROR!";
        else if (error_code === 403)
            content = " FORBIDDEN ERROR!";
        else if (error_code === 401)
            content = " UNAUTHORIZED ERROR!";
        let node = document.createTextNode(error_code + content);        
        document.getElementsByClassName("error-content")[0].appendChild(node);
    }
});