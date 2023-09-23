$(function(){
    var alerts=$("#main");
    alerts.empty();
    $.get("/newbills", function(data){
        if(data=="no")
            console.log("no new bills")
        else{
            alerts.append("<h2>REMINDERS</h2>")
            alerts.append(data);
            }
    });
});
function fout(event){
    var main=$("#main");
    $(main).fadeOut(2000);
}
function showbill(event){
    var billid=event.target.id;
    $.get( "/billdetails",{bill_id:billid} );
}