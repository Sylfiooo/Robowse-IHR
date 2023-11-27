$(document).ready(function () {
    session = new QiSession();

    $('#page_empty').show();
    $('#page_low_love').hide();
    $('#page_medium_love').hide();
    $('#page_high_love').hide();
    $('#page_wow_love').hide(); 
    $('#page_no_love').hide();   


    function raise(event, value) {
        session.service("ALMemory").done(function(ALMemory) {
            ALMemory.raiseEvent(event, value);
        });
    }

    session.service("ALMemory").done(function(ALMemory) {

        ALMemory.subscriber("Robowse/Page/LowLove").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_empty').hide();
                $('#page_low_love').show();
                $('#page_medium_love').hide(); 
                $('#page_high_love').hide();
                $('#page_wow_love').hide(); 
                $('#page_no_love').hide();  
            });
        });

        ALMemory.subscriber("Robowse/Page/MidLove").done(function(subscriber) {

            subscriber.signal.connect(function() {     
                $('#page_empty').hide();
                $('#page_low_love').hide();
                $('#page_medium_love').show(); 
                $('#page_high_love').hide();
                $('#page_wow_love').hide(); 
                $('#page_no_love').hide();  
            });
        });

        ALMemory.subscriber("Robowse/Page/HighLove").done(function(subscriber) {

            subscriber.signal.connect(function() {  
                $('#page_empty').hide();
                $('#page_low_love').hide();
                $('#page_medium_love').hide(); 
                $('#page_high_love').show();
                $('#page_wow_love').hide(); 
                $('#page_no_love').hide();  
            });
        });
        
        ALMemory.subscriber("Robowse/Page/NoLove").done(function(subscriber) {

            subscriber.signal.connect(function() {  
                $('#page_empty').hide();
                $('#page_low_love').hide();
                $('#page_medium_love').hide(); 
                $('#page_high_love').hide();
                $('#page_wow_love').hide(); 
                $('#page_no_love').show();  
            });
        });

        ALMemory.subscriber("Robowse/Page/WowLove").done(function(subscriber) {

            subscriber.signal.connect(function() {  
                $('#page_empty').hide();
                $('#page_low_love').hide();
                $('#page_medium_love').hide(); 
                $('#page_high_love').hide();
                $('#page_wow_love').show(); 
                $('#page_no_love').hide();  
            });
        });

    });

});
