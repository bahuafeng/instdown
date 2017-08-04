function load_resource(api){
    instgram_url = encodeURIComponent($("#instgram_url").val());
    $.ajax({  
        type: "GET",  
        url: api,  
        data: "url="+instgram_url,

        success: function(data) {  
            if(data != "") {
                data = $.parseJSON(data);
                if (data.data.video != null){
                    $("#video").html(
                        "<video src='" + data.data.video + "' controls='controls' class='center-block' width='400px'></video>" +
                        "<a href='" + data.data.video + "' download ><button type='button' class='btn btn-primary btn-lg center-block' style='width: 400px;'>Download video</button></a>"
                    );
                }
                if (data.data.image != null){
                    $("#image").html(
                        "<img src='" + data.data.image + "' class='thumbnail img-responsive center-block' width='400px' alt=></img>" +
                        "<a href='" + data.data.image + "' download ><button type='button' class='btn btn-primary btn-lg center-block' style='width: 400px;'>Download photo</button></a>"
                    );
                }
            }else {  
                alert("fail comment!");  
            }  
        }  
    });  
};
