var questions = {
    show_result: function() {
        $("#aswr-score-num").html(this.round_score);
        $("#total-score-num").html(this.user_score + this.round_score);
        $("#qstn").hide();
        $("#aswr-rslt").css("display", "flex").fadeIn(900);
    },
    show_question: function(i) {
        var $this = this;
        if(i >= $this.questions.length) {
            $this.show_result();
            return;
        }
        var question = $this.questions[i];
        console.log(question);
        var qstn_content = (i+1).toString() + ". " + question.question_text;
        var qstn_score = question.score + "分";
        var count_down = question.count_down;
        var options_html = "";
        for(var j=0;j<question.options.length;j++) {
            var option = question.options[j];
            options_html += '<div class="border border-secondary rounded-pill opt-content">' + option.label + ". " + option.option_text + '</div>\n';
        }
        $("#qstn-clock").html(count_down);
        $("#qstn-content").html(qstn_content);
        $("#qstn-score").html(qstn_score);
        $("#options").html(options_html);
        $("#qstn-opts").show();

        count_down = 1;
        var ret = setInterval(function() {
            if(count_down == -1) {
                var msg = "时间到";
                $("#qstn-modal-body").html(msg);
                $("#qstn-modal").modal("show");
                clearInterval(ret);
                setTimeout(function() {
                    $("#qstn-modal").modal("hide");
                }, 1000);
                setTimeout(function() {
                    $this.show_question(i+1);
                }, 1200);
                return;
            }
            $("#qstn-clock").html(count_down);
            count_down = count_down - 1;
        }, 1000);
    },
    prepare_countdown: function(num) {
        var $this = this;
        var ret = setInterval(function() {
            if(num == 0) {
                clearInterval(ret);
                $this.show_question(4);
                return;
            }
            $("#prepare").html(num);
            $("#prepare").fadeIn(900, function(){
                $("#prepare").hide();
            });
            num = num - 1;
        }, 1000);
    },
    get_questions: function() {
        var $this = this;
        $.ajax({
            type: "GET",
            url: "/get_random_questions/",
        }).done(function(data) {
            if(data.success) {
                $this.questions = data.result.questions;
                $this.user_score = data.result.user_score;
            }
            else {
                var msg = "服务器开小差了";
                $("#qstn-modal-body").html(msg);
                $("#qstn-modal").modal("show");
            }
        });
    },
    init: function() {
        this.get_questions();
        this.prepare_countdown(3);
        this.round_score = 0;
    },
}
