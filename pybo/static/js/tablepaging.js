function pagination(){
        var req_num_row=5;
        var $tr=jQuery('#disease tbody tr');
        var total_num_row=$tr.length;
        var num_pages=0;
        if(total_num_row % req_num_row ==0){
            num_pages=total_num_row / req_num_row;
        }
        if(total_num_row % req_num_row >=1){
            num_pages=total_num_row / req_num_row;
            num_pages++;
            num_pages=Math.floor(num_pages++);
        }

    // jQuery('.pagination').append("<button class=\"prev\">Prev</button>");

        for(var i=1; i<=num_pages; i++){
            jQuery('.pagination').append("<button class='page'>"+i+"</button>");
            jQuery('.pagination button:nth-child(2)').addClass("active");
            jQuery('.pagination a').addClass("pagination-link");
        }

    // jQuery('.pagination').append("<button class=\"next\">Next</button>");

    $tr.each(function(i){
        jQuery(this).hide();
        if(i+1 <= req_num_row){
            $tr.eq(i).show();
        }
    });

    jQuery('.pagination button').click('.pagination-link', function(e){
        e.preventDefault();
        $tr.hide();
        var page=jQuery(this).text();   // 현재 페이지 번호 정의
        var prevpage=page-1;        //이전 페이지 번호 정의
        var temp=page-1;        // 페이지번호-1 정의 -> 버튼 위치 찾기위함
        var start=temp*req_num_row;
        var current_link = temp;

        jQuery('.pagination button').removeClass("active");
        jQuery(this).parent().addClass("active");

        // 버튼을 누를 때 현재페이지만 비활성화 상태로 전환
        jQuery('.pagination button.disabled').removeClass("disabled");
        jQuery(this).addClass("disabled")
        
        
        // 각 tr을 해당 위치부터 지정된 갯수만큼 보여주기
        for(var i=0; i< req_num_row; i++){
            $tr.eq(start+i).show();
        }



        // if(temp >= 1){
        //     jQuery('.pagination button:first-child').removeClass("disabled");
        // }
        // else {
        //     jQuery('.pagination button:first-child').addClass("disabled");
        // }
            
    });
    // 이전 버튼 클릭 동작
    // jQuery('.prev').click(function(e){
    //     e.preventDefault();
    //     jQuery('.pagination button:first-child').removeClass("active");
    // });
    // // 다음 버튼 클릭 동작
    // jQuery('.next').click(function(e){
    //     e.preventDefault();
    //     jQuery('.pagination button:last-child').removeClass("active");
    // });

    }

jQuery('document').ready(function(){
    pagination();

    jQuery('.pagination button:first-child').addClass("disabled");

});