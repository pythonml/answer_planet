var questions = {
    show_result: function() {
        $("#aswr-score-num").html(this.round_score);
        $("#total-score-num").html(this.user_score + this.round_score);
        $("#qstn").hide();
        $("#aswr-rslt").css("display", "flex").fadeIn(900);
    },
    show_question: function() {
        var $this = this;
        if($this.qstn_id >= $this.questions.length) {
            $this.show_result();
            return;
        }
        var question = $this.questions[$this.qstn_id];
        console.log(question);
        var qstn_content = ($this.qstn_id+1).toString() + ". " + question.question_text;
        var qstn_score = question.score + "分";
        var count_down = question.count_down;
        var options_html = "";
        for(var j=0;j<question.options.length;j++) {
            var option = question.options[j];
            options_html += '<div class="border border-grey rounded-pill opt-content" option-id="' + option.option_id + '"onclick="questions.submit_answer(event)">' + option.label + ". " + option.option_text + '</div>\n';
        }
        $("#qstn-clock").html(count_down);
        $("#qstn-content").html(qstn_content);
        $("#qstn-score").html(qstn_score);
        $("#options").html(options_html);
        $("#qstn-opts").show();
        $this.qstn_id += 1;

        count_down = 10;
        $this.intv = setInterval(function() {
            if(count_down == -1) {
                var msg = "时间到";
                $("#qstn-modal-body").html(msg);
                $("#qstn-modal").modal("show");
                clearInterval($this.intv);
                setTimeout(function() {
                    $("#qstn-modal").modal("hide");
                }, 1000);
                setTimeout(function() {
                    $this.show_question();
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
        this.qstn_id = 0;
    },
    highlight_correct: function(select_opt, correct_opt) {
        var target = $('div[option-id="' + select_opt +'"]');
        target.removeClass("border-warning text-warning").addClass("border-success bg-success text-white")
    },
    highlight_wrong: function(select_opt, correct_opt) {
        var target = $('div[option-id="' + select_opt +'"]');
        target.removeClass("border-warning text-warning").addClass("border-danger bg-danger text-white")
    },
    update_score: function() {
        var score = parseInt($("#qstn-score").html());
        this.round_score += score;
        $("#score-num").html(this.round_score);
    },
    submit_answer: function(event) {
        var $this = this;
        var target = $(event.target);
        target.removeClass("border-grey").addClass("border-warning text-warning");
        var option_id = target.attr("option-id");
        $.ajax({
            type: "POST",
            url: "/answer/submit/",
            data: {"option_id": option_id}
        }).done(function(data) {
            if(data.success) {
                var is_correct = data.result.is_correct;
                var correct_option = data.result.correct_option;
                if(is_correct) {
                    $this.highlight_correct(option_id, correct_option);
                    $this.update_score();
                }
                else {
                    $this.highlight_wrong(option_id, correct_option);
                }
                clearInterval($this.intv);
                setTimeout(function() {
                    $this.show_question();
                }, 200);
            }
            else {
                var msg = "服务器开小差了";
                $("#aswrrslt-modal-body").html(msg);
                $("#aswrrslt-modal").modal("show");
            }
        });
    }
}
