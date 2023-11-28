$(document).ready(function () {
    session = new QiSession();

    $('#page_start').show();
    $('#page_menu').hide();
    $('#page_love').hide();
    $('#page_food').hide();
    $('#page_jul').hide();


    function raise(event, value) {
        session.service("ALMemory").done(function(ALMemory) {
            ALMemory.raiseEvent(event, value);
        });
    }

    session.service("ALMemory").done(function(ALMemory) {

        ALMemory.subscriber("Robowse/Page/Menu").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_start').hide();
                $('#page_menu').show();
                $('#page_love').hide();
                $('#page_food').hide();
                $('#page_jul').hide();
            });
        });

        ALMemory.subscriber("Robowse/Page/Love").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_menu').hide();
                $('#page_love').show();
            });
        });

        ALMemory.subscriber("Robowse/Page/Food").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_menu').hide();
                $('#page_food').show();
                raise('Robowse/Nourriture', 1);
            });
        });

        ALMemory.subscriber("Robowse/Page/Jul").done(function(subscriber) {

            subscriber.signal.connect(function() {
                $('#page_menu').hide();
                $('#page_jul').show();
            });
        });

    });

    $('#btn_start').on('click', function() {
        raise('Robowse/Start', 1);
    });

    $('#select_love').on('click', function() {
        console.log("Choose Love");
        raise('Robowse/ChooseLove', 1);
    });

    $('#select_food').on('click', function() {
        console.log("Choose Food");
        raise('Robowse/ChooseFood', 1);
    });

});
