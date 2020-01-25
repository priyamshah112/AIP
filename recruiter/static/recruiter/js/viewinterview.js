var questions = [
    {
        no: "1",
        question: "what are your hobbies",
        video: "https://www.youtube.com/embed/dhYOPzcsbGM",
        grade: 9,
        comments: "comment1"
    },
    {
        no: "2",
        question: "what are your interests",
        video: "https://www.youtube.com/embed/r2LpOUwca94",
        grade: 8,
        comments: "comment2"
    },
    {
        no: "3",
        question: "what are your skills",
        video: "https://www.youtube.com/embed/V5M2WZiAy6k",
        grade: 9,
        comments: "comment3"
    },
];

var videoframe = $('#videoframe');
var question_text = $('#question-text');
var comment_text = $('#comment');
var current_question = 1;

function change_question() {
    var new_question = parseInt(this.id.slice(-1));
    var temp_new = questions[new_question - 1];
    var temp_current = questions[current_question - 1];
    $(this).parent().toggleClass('active');
    $('#ques-' + current_question).parent().toggleClass('active');
    videoframe.attr("src", temp_new.video);
    question_text.text(temp_new.question);
    $('#grade :nth-child(' + temp_new.grade + ')').toggleClass('btn-outline-success btn-success');
    $('#grade :nth-child(' + temp_current.grade + ')').toggleClass('btn-outline-success btn-success');
    comment_text.text(temp_new.comments);
    current_question = new_question;
}

function change_grade() {
    var temp_current = questions[current_question - 1];
    $('#grade :nth-child(' + temp_current.grade + ')').toggleClass('btn-outline-success btn-success');
    $(this).toggleClass('btn-outline-success btn-success');
    var new_grade = parseInt($(this).text());
    temp_current.grade = new_grade;
}

$('[id^=ques-').on('click', change_question);
$('#grade').on('click', 'button', change_grade);