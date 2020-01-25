

function packageOnClickListener() {
    $('#dropdownMenuLinkselect.dropdown-menu a').on('click', function () {
        changePackage($(this)[0].innerText);
        $('#dropdownMenuLink').html($(this).html());

    });
}
  packageOnClickListener();

    $('#builtInQuestions').on('change', function () {
        let questionType = this.value;
        loadQuestions(questionType);
    });
    $("#addPackageBtn").click(function () {
        let packageName = $("#package1").val();
        let questionType = $("#questionType1").val();
        let question = $("#question1").val();
        $('#exampleModalCenter1').modal('hide')
        addPackage(packageName, questionType, question);
        $('#dropdownMenuLink').text(packageName);
    });

    $("#addQuestionBtn").click(function () {
        let packageName = $("#dropdownMenuLink")[0].innerText;
        let questionType = $("#questionType").val();
        let question = $("#question").val();
        $('#exampleModalCenter').modal('hide')
        addQuestion(packageName, questionType, question);

    });

    function addClickListener() {
        $(".delete-btn").click(function () {
            let packageName = $("#dropdownMenuLink")[0].innerText;

            deleteQuestion(this.id, packageName);


        });
    }

    addClickListener();


    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    // function for sending request to add package
    function addPackage(packageName, questionType, question) {

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    // Send the token to same-origin, relative URLs only.
                    // Send the token only if the method warrants CSRF protection
                    // Using the CSRFToken value acquired earlier
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        data = {
            'packageName': packageName,
            'question': question,
            'questionType': questionType
        }
        $.ajax({
            url: 'addpackage',
            type: 'POST',
            dataType: "json",
            data: data,
            success: function (data) {
                //window.location.reload();
                changePackage(packageName);
                getPackages();
            }

        });
    }


    // function for sending request to add package
    function addQuestion(packageName, questionType, question) {

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    // Send the token to same-origin, relative URLs only.
                    // Send the token only if the method warrants CSRF protection
                    // Using the CSRFToken value acquired earlier
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        data = {
            'packageName': packageName,
            'question': question,
            'questionType': questionType
        }
        $.ajax({
            url: 'addquestion',
            type: 'POST',
            dataType: "json",
            data: data,
            success: function (data) {
                // window.location.reload();
                changePackage(packageName);
            }

        });
    }



    // function for sending request to add package
    function deleteQuestion(qid, packageName) {

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    // Send the token to same-origin, relative URLs only.
                    // Send the token only if the method warrants CSRF protection
                    // Using the CSRFToken value acquired earlier
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        data = {
            'id': qid,
            'packageName': packageName
        }
        $.ajax({
            url: 'deletequestion',
            type: 'POST',
            dataType: "json",
            data: data,
            success: function (data) {
                // window.location.reload();
                changePackage(packageName);
            }

        });
    }

    // function for sending request to change cuurent  package
    function changePackage(packageName) {

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    // Send the token to same-origin, relative URLs only.
                    // Send the token only if the method warrants CSRF protection
                    // Using the CSRFToken value acquired earlier
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        data = {
            'packageName': packageName,
        }
        $.ajax({
            url: 'changepackage',
            type: 'POST',
            dataType: "json",
            data: data,
            success: function (data) {
                $('#sortable').empty(); // empty the div before fetching and adding new data
                $("#rightLoader").show();

                data.user_questions.forEach((item, index) => {
                    $("#sortable").append(
                        `<div name=${item.type} draggable="true" class="fill shadow-sm p-2 mb-2 bg-white rounded  ">
                      ${item.question}   
                      
                      <button id=${item.id} class="delete-btn btn float-right"><i
                      class="fas fa-trash-alt"></i></button>
                      </div>
                      `
                    );
                }
                );

                addClickListener();
                $("#rightLoader").hide();


            }

        });
    }

    // function for sending request to fetch buitin questions by category
    function loadQuestions(questionType) {

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    // Send the token to same-origin, relative URLs only.
                    // Send the token only if the method warrants CSRF protection
                    // Using the CSRFToken value acquired earlier
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        data = {
            'questionType': questionType,
        }
        $.ajax({
            url: 'loadquestions',
            type: 'POST',
            dataType: "json",
            data: data,
            success: function (data) {

                $('#builtInQuestionsArea').empty(); // empty the div before fetching and adding new data

                data.built_in_questions.forEach((item, index) => {
                    $("#builtInQuestionsArea").append(
                        `<div id='${item.id}'  name ='${item.type}' draggable="true" class=" fill shadow-sm p-2 mb-2 bg-white rounded">
                        ${item.question}   
                        </div>`
                    );
                }

                );

                setDragEventListener();

            }

        });
    }
    // function for sending request to fetch buitin questions by category
    function getPackages() {

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    // Send the token to same-origin, relative URLs only.
                    // Send the token only if the method warrants CSRF protection
                    // Using the CSRFToken value acquired earlier
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        $.ajax({
            url: 'getPackages',
            type: 'GET',
            dataType: "json",
            success: function (data) {
                $('#dropdownMenuLinkselect').empty(); // empty the div before fetching and adding new data

                data.user_packages.forEach((item, index) => {
                    $("#dropdownMenuLinkselect").append(
                        `
                        <a class="dropdown-item" href="#">${item}</a>

                        `
                    );
                }

                );
                packageOnClickListener();

            }

        });
    }
    // function for sending request to fetch buitin questions by category
    function loadQuestions(questionType) {

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                    // Send the token to same-origin, relative URLs only.
                    // Send the token only if the method warrants CSRF protection
                    // Using the CSRFToken value acquired earlier
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        data = {
            'questionType': questionType,
        }
        $.ajax({
            url: 'loadquestions',
            type: 'POST',
            dataType: "json",
            data: data,
            success: function (data) {

                $('#builtInQuestionsArea').empty(); // empty the div before fetching and adding new data

                data.built_in_questions.forEach((item, index) => {
                    $("#builtInQuestionsArea").append(
                        `<div id='${item.id}'  name ='${item.type}' draggable="true" class=" fill shadow-sm p-2 mb-2 bg-white rounded">
                ${item.question}   
                </div>`
                    );
                }

                );

                setDragEventListener();

            }

        });
    }



    ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////


    if (window.history.replaceState) {

        window.history.replaceState(null, null, window.location.href);

    }

    const empties = document.querySelectorAll('.empty');
    function setDragEventListener() {
        let fills = document.querySelectorAll('.fill');

        for (const fill of fills) {
            // Fill listeners
            fill.addEventListener('dragstart', dragStart);
            fill.addEventListener('dragend', dragEnd);
        }
    };
    setDragEventListener();

    // Loop through empty boxes and add listeners
    for (const empty of empties) {
        empty.addEventListener('dragover', dragOver);
        empty.addEventListener('dragenter', dragEnter);
        empty.addEventListener('dragleave', dragLeave);
        empty.addEventListener('drop', dragDrop);
    }

    // Drag Functions

    function dragStart() {
        // this.className += ' hold';
        event.dataTransfer.setData("Text", event.target.id);

        // setTimeout(() => (this.className = 'invisible'), 0);
    }

    function dragEnd() {

        //  this.className = 'fill';

    }

    function dragOver(e) {

        e.preventDefault();
    }

    function dragEnter(e) {

        e.preventDefault();
        //this.className += ' hovered';
    }

    function dragLeave() {

        // this.className = 'empty';
    }

    function dragDrop(event, el) {

        var data = event.dataTransfer.getData("Text");
        // this.className = 'empty';
        sourcenode = document.getElementById(data);
        appendnode = sourcenode.cloneNode(true);
        appendnode.setAttribute('id', 'q' + data);
        let packageName = $("#dropdownMenuLink")[0].innerText;
        let question = appendnode.innerText.trim();
        let questionType = appendnode.getAttribute("name");
        $("#rightLoader").show();

        addQuestion(packageName, questionType, question);


        this.appendChild(appendnode);
        $("#rightLoader").hide();



    }

    $(document).ready(function () {
        $("#sortable").sortable();
        $("#sortable").disableSelection();
    });

