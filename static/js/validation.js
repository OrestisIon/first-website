
    function buttonRegister() {
        var alerts= $("#alerts");
        var ispost=true;
        alerts.empty();
        var username = $('#username').val();
        if (username==null || username=="") {
            alerts.append("<p>Username must be filled in<p>");
            ispost=false;
        }
        var email = $('#email').val();
        console.log(email);
        if (email==null || email=="") {
            alerts.append("<p>Email must be filled in</p>");
            ispost=false;
        }
        var pass = $('#password').val();
        console.log(pass);
        if (pass==null || pass=="") {
            alerts.append("<p>Password must be filled in</p>");
            ispost=false;
        }
        else{
            if(pass.length<8){
            alerts.append("<p>Password must be more than 8 characters long</p>");
            ispost=false;
            }
        }
        var pass2 = $('#password2').val();
        console.log(pass2);
        if(pass != pass2 ){
            alerts.append("<p>Password does not match confirmation</p>");
            ispost=false;
        } 
        if(ispost==true){
            $.post("/registration",
            {"username":username,"email":email, "password":pass},
            function(data){
                window.location = "/";
                }
            )
        }
    };
function login(event) {
        event.preventDefault();
        var alerts= $("#alerts");
        var ispost=true;
        alerts.empty();
        var email = $('#email').val();
        if (email==null || email=="") {
            alerts.append("<p>Email must be filled in</p>");
            ispost=false;
        }
        var pass = $('#password').val();
        if (pass==null || pass=="") {
            alerts.append("<p>Password must be filled in</p>");
            ispost=false;
        }
        else{
            if(pass.length<8){
            alerts.append("<p>Password must be more than 8 characters long</p>");
            ispost=false;
            }
        }
        if(ispost==true){
            $.post("/login",
            {"email":email, "password":pass},
            function(data){
                if(data=="ok"){
                    window.location = "/"; //as found from this website - https://stackoverflow.com/questions/5651933/what-is-the-opposite-of-evt-preventdefault
                }
                else{
                    alerts.append(data);
                }
                
        });
        }    
};
    var groupid;
    function submitButtonClick(event) {
        event.preventDefault();
        var alerts= $("#alerts");
        var ispost=true;
        alerts.empty();
        var name = $('#groupname').val();
        if (name==null || name=="") {
            alerts.append("<p>Group name must be filled in<p>");
            ispost=false;
        }
        if(ispost==true){
            $.post("/addgroup",
            {"name":name},
            function(data){
                if(data=="Group name already exist. Try new one!")
                   alerts.append(data); //making the string id to integer to be able to use it
                else{
                    groupid=parseInt(data);
                    ChangeTemplate();
                }         
            });
        }
    };

    function ChangeTemplate() {
        $(".create_group").toggle();
        $(".remove").toggle();
        $(".add_group_members").toggle();
    }
    function ChangeButton(id) {
        var elem1= document.getElementsByClassName("add"+id);
        var elem2= document.getElementsByClassName("remove"+id);
        console.log(elem1);
        $(elem1).toggle();
        $(elem2).toggle();
    };
    function addButton(event){
        var alerts= $("#alerts1");
        alerts.empty();
        var user_email=event.target.id; //getting the id of the element that was clicked
        console.log(user_email);
            $.post("/addgroup_members",
                {"group_id":groupid, "user_email":user_email},
                function(data){ 
                    alerts.append(data);
                    ChangeButton(user_email);
                });
    };

    function removeButton(event){
        var user_email=event.target.id;
         $.post("/remove_members",
             {"group_id":groupid,"user_email":user_email},
             function(data){
                 console.log(data);
                 ChangeButton(user_email);
         });
     };