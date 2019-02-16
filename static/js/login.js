var login = {
    "init": function() {
        this.username = "";
        this.password = "";
    },
    "update_username": function(event) {
        this.username = $(event.target).val();
        if(this.username.length > 0) {
            $("#username-err").hide();
        }
    },
    "update_password": function(event) {
        this.password = $(event.target).val();
        if(this.password.length > 0) {
            $("#password-err").hide();
        }
    },
    "submit": function (event) {
        err = false;
        if(this.username.length == 0) {
            $("#username-err").html("用户名不能为空");
            $("#username-err").show();
            err = true;
        }
        if(this.password.length == 0) {
            $("#password-err").html("密码不能为空");
            $("#password-err").show();
            err = true;
        }
        if(err) {
            return;
        }

        $.ajax({
            type: "POST",
            url: "/auth/",
            data: {"username": this.username, "password": this.password}
        }).done(function(data) {
            if(data.success) {
            }
            else {
				$("#login-modal-body").html(data.msg);
				$("#login-modal").modal("show");
				setTimeout(function() {
					window.location.reload();
				}, 2000);
            }
        });
    }
}
