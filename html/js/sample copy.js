$(document).ready(function () {
    session = new QiSession();

    $('#page_start').show();
    $('#page_selection').hide();
    $('#page_YesNo').hide(); 

    $('#page_selection_ukraine_selec').hide();
    $('#page_selection_russie_selec').hide();   


    function raise(event, value) {
        session.service("ALMemory").done(function(ALMemory) {
            ALMemory.raiseEvent(event, value);
        });
    }

    session.service("ALMemory").done(function(ALMemory) {

        ALMemory.subscriber("Robowse/Page/Empty").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_selection').hide();
                $('#page_start').hide();
                $('#page_YesNo').hide(); 
            });
        });


        ALMemory.subscriber("Robowse/Page/Selection").done(function(subscriber) {

            subscriber.signal.connect(function() {     
                $('#page_start').hide();          
                $('#page_selection').show();
                $('#page_YesNo').hide(); 
            });
        });

        ALMemory.subscriber("Robowse/Page/Start").done(function(subscriber) {

            subscriber.signal.connect(function() {  
                $('#page_start').show();             
                $('#page_selection').hide();
                $('#page_YesNo').hide(); 
            });
        });        


        ALMemory.subscriber("Robowse/Page/YesNo").done(function(subscriber) {

            subscriber.signal.connect(function() {  
                $('#page_start').hide();             
                $('#page_selection').hide();
                $('#page_YesNo').show(); 

                $('#page_selection_ukraine_selec').hide();
                $('#page_selection_russie_selec').hide();               
            });
        });         


        ALMemory.subscriber("Robowse/Select").done(function(subscriber) {

            subscriber.signal.connect(function() {

                ALMemory.getData("Robowse/Select").then(function(data) {
                    data=="U"  ?    $('#page_selection_ukraine_selec').show() : $('#page_selection_ukraine_selec').hide(); // permet d'afficher ou non "is chosen" pour le choix 1
                    data=="R"  ?    $('#page_selection_russie_selec').show() : $('#page_selection_russie_selec').hide();
                    console.log(data) // permet d'afficher ou non "is chosen" pour le choix 2
                    raise('Robowse/Next', 1);
                }, console.log("select select"));
                console.log("raise");

                raise('Robowse/Next', 1);


            });
        });        

    });



	$('#page_start').on('click', function() {
        console.log("click Start");
        raise('Robowse/Start', 1)
    });

    $('#page_selection_ukraine').on('click', function() {
        console.log("click 1");
        raise('Robowse/Button1', 1)
    });

    $('#page_selection_russie').on('click', function() {
        console.log("click 2");
        raise('Robowse/Button2', 1)      
    });



    $('#page_yes').on('click', function() {
        console.log("click ButtonYes");
        raise('Robowse/ButtonYes', 1)      
    });

    $('#page_no').on('click', function() {
        console.log("click ButtonNo");
        raise('Robowse/ButtonNo', 1)       
    });    


});
