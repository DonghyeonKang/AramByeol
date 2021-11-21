fetch('#').then(function(response){
    const error_code = response['status'];
    let content="";
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