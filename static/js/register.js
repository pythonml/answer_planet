var register = {
    "init": function() {
        this.username = "";
        this.password = "";
        this.pwdconfirm = "";
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
    "update_pwdconfirm": function(event) {
        this.pwdconfirm = $(event.target).val();
        if(this.pwdconfirm.length > 0) {
            $("#pwdconfirm-err").hide();
        }
    },
    "submit": function() {
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
        if(this.pwdconfirm.length == 0) {
            $("#pwdconfirm-err").html("请再次输入密码");
            $("#pwdconfirm-err").show();
            err = true;
        }
        if(this.pwdconfirm != this.password) {
            $("#pwdconfirm-err").html("两次输入的密码不同");
            $("#pwdconfirm-err").show();
            err = true;
        }
        if(err) {
            return;
        }

        $.ajax({
            type: "POST",
            url: "/user/create/",
            data: {"username": this.username, "password": this.password, "pwdconfirm": this.pwdconfirm}
        }).done(function(data) {
            if(data.success) {
                var msg = "注册成功";
                $("#reg-modal-body").html(msg);
                $("#reg-modal").modal("show");
                setTimeout(function() {
                    url = "/menu/";
                    window.location.replace(url);
                }, 2000);
            }
            else {
				$("#reg-modal-body").html(data.msg);
				$("#reg-modal").modal("show");
				setTimeout(function() {
					window.location.reload();
				}, 2000);
            }
        });
    }
};
