const url = window.location.href.split('/');
const protocol = url[0];
const domain = url[2];


$(document).ready(function() {
    // send message
    $('#send-btn').click(function () {
        let pattern = $('#send').val();
        // display message
        displayMessage(pattern);

        let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

        let payload = {
            "url": `http://127.0.0.1:8000/api/v1.0/medibot/`,
            "method": "POST",
            "timeout": 0,
            "dataType": "json",
            "data": {
                "csrfmiddlewaretoken": csrf_token,
                'pattern': pattern,
            }
        };

        callChatBotEndPoints(payload);
    });


    // call cart end points
    function callChatBotEndPoints(payload) {
        $.ajax(payload).done(function (response) {
            console.log(response);
            displayChatBotResponse(response);
            // updateCartIcon(response['Item Count'])
        });
    }

    // display user message
    function displayMessage(msg){
        $('#chat-container').append(
            `
                <div class="col mb-2">
                    <div class="row">
                        <div class="col col-10 col-sm-11 rounded-pill bg-success p-2 text-light">
                           <div class="ms-2">
                                ${msg}
                           </div>
                        </div>
                        <div class="col col-2 col-sm-1">
                            <i class="fa fa-user-circle-o fa-2x" aria-hidden="true"></i>
                        </div>
                    </div>
                </div>
            `
        );
    }

    // display chatbot response
    function displayChatBotResponse(response){
        $('#chat-container').append(
            `
                <div class="col mb-2">
                    <div class="row">
                        <div class="col col-2 col-sm-1 ">
                            <i class="fa fa-user-circle-o fa-2x" aria-hidden="true"></i>
                        </div>
                        <div class="col col-10 col-sm-10 rounded-pill bg-success p-2 text-light">
                           <div class="ms-2">
                                 ${response['response']}
                           </div>
                        </div>
                    </div>
                </div>
            `
        );
        if (!(response['followup_questions'] == null)){
            response['followup_questions'].forEach(function ())
        }
    }

    // remove send button
    function removeSendButton(){
        $('#send-btn').remove();
        $('#send-form').append(
            `
                <div class="col col-2 col-sm-2" id="answer-btn">
                      <button type="button" class="btn btn-primary mb-3">
                        <i class="fa fa-paper-plane" aria-hidden="true"></i>
                      </button>
                    </div>
            `
        );

    }

    // add send button
    function addSendButton(){
        $('#answer-btn').remove();
        $('#send-form').append(
            `
                <div class="col col-2 col-sm-2" id="send-btn">
                      <button type="button" class="btn btn-primary mb-3">
                        <i class="fa fa-paper-plane" aria-hidden="true"></i>
                      </button>
                    </div>
            `
        );

    }

    function showAppointmentCard(doctors){
        $('#chat-container').append(
            `
                <div class="card">
                  <h5 class="card-header">Featured</h5>
                  <div class="card-body">
                    <h5 class="card-title">Special title treatment</h5>
                    <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
                    <a href="#" class="btn btn-primary">Go somewhere</a>
                  </div>
                </div>
            `
        );
    }

});