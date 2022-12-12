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

    jQuery('.pagination').append("<button class=\"prev\">Prev</button>");

        for(var i=1; i<=num_pages; i++){
            jQuery('.pagination').append("<button>"+i+"</button>");
            jQuery('.pagination button:nth-child(2)').addClass("active");
            jQuery('.pagination a').addClass("pagination-link");
        }

    jQuery('.pagination').append("<button class=\"next\">Next</button>");

    $tr.each(function(i){
        jQuery(this).hide();
        if(i+1 <= req_num_row){
            $tr.eq(i).show();
        }
    });

    jQuery('.pagination button').click('.pagination-link', function(e){
        e.preventDefault();
        $tr.hide();
        var page=jQuery(this).text();
        var prevpage=page-1;        //이전 페이지 번호 정의
        var temp=page-1;
        var start=temp*req_num_row;
        var current_link = temp;

        jQuery('.pagination button').removeClass("active");
        jQuery(this).parent().addClass("active");
        

        for(var i=0; i< req_num_row; i++){
            $tr.eq(start+i).show();
        }



        if(temp >= 1){
            jQuery('.pagination button:first-child').removeClass("disabled");
        }
        else {
            jQuery('.pagination button:first-child').addClass("disabled");
        }
            
    });

    jQuery('.prev').click(function(e){
        e.preventDefault();
        jQuery('.pagination button:first-child').removeClass("active");
    });

    jQuery('.next').click(function(e){
        e.preventDefault();
        jQuery('.pagination button:last-child').removeClass("active");
    });

    }

jQuery('document').ready(function(){
    pagination();

    jQuery('.pagination button:first-child').addClass("disabled");

});