function load_resource(api){
    instagram_url = encodeURIComponent($("#instagram_url").val());
    $.ajax({  
        type: "GET",  
        url: api,  
        data: "url="+instagram_url,

        success: function(data) {  
            if(data != "") {
                data = $.parseJSON(data);
                if (data.data.video != null){
                    $("#video").html(
                        "<video src='" + data.data.video + "' controls='controls' class='center-block' width='400px'></video>" +
                        "<a href='" + data.data.video + "' download ><button type='button' class='btn btn-primary btn-lg center-block' style='width: 400px;'>Download video</button></a>"
                    );
                }else{
                    $("#video").html("");
                }
                if (data.data.image != null){
                    $("#image").html(
                        "<img src='" + data.data.image + "' class='thumbnail img-responsive center-block' width='400px' alt=></img>" +
                        "<a href='" + data.data.image + "' download ><button type='button' class='btn btn-primary btn-lg center-block' style='width: 400px;'>Download photo</button></a>"
                    );
                }else{
                    $("#image").html("");
                }
            }else {  
                alert("fail comment!");  
            }  
        }  
    });  
};
