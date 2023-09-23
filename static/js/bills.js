var billid;
$(function () {
    $(".Choose_Group").toggle();
    $(".final").toggle();
    billid=0;
});
function changeTemp(){
    $(".bill_details").toggle();
    $(".Choose_Group").toggle();
}
function changeTemp2(){
    $(".Choose_Group").toggle();
    $(".final").toggle();
}

function submitdetails(event){
    event.preventDefault();
    var alerts= $("#alerts");
    alerts.empty();
    var ispost=true;
    var name = $('#name').val();
    var amount = $('#amount').val();
    if (name==null || name=="") {
        alerts.append("<p>Name of bill must be filled in</p>");
        ispost=false;
    }
    if (amount==null || amount=="") {
        alerts.append("<p>Amount of bill must be filled in</p>");
        ispost=false;
    }
    if(ispost==true){
        $.post("/addbill",
            {"billname":name, "amount":amount},
            function(data){ 
                if((data=="fail1") || (data=="fail2")){
                    console.log(data);
                    alerts.append("<p>Bill name already exists<p>");
                }
                else{
                    billid=parseInt(data);
                    changeTemp();
                }
        });
    }
    
};

function addGroup(event){
    event.preventDefault();
    var alerts= $("#alerts");
    alerts.empty();
    var group_id=parseInt(event.target.id); //getting the id of the element that was clicked
    console.log(billid);
    console.log(group_id);
    $.post("/addgroup_tobill",
        {"group_id":group_id, "bill_id":billid},
        function(data){ 
            if(data="ok")
                changeTemp2();
            else
                alerts.append(data);   
        });
};
