// 客户端 Markdown 渲染
function run() {
  // 尽量避免 var 的使用，改用 let
  // 获取 id 为 body 里面的文本
  let text = $("#body").val(),
    // 开启表格和删除线功能（因为默认是关闭的）
    converter = new showdown.Converter({
      tables: true,
      strikethrough: true
    }),
    // Markdown 文本转换成 html
    html = converter.makeHtml(text);

  // 选取并覆盖 html
  $("#MDOut").html(html);
}

// JQuery绑定textarea的改变事件
$("#body").bind("input propertychange", () => {
  run();
});

// 验证码的校验系统
$.ajax({
  // 先通过远程服务器 get_captcha 脚本，获取必须的验证信息
  url: "/cgi-bin/get_captcha.py",
  type: "get",
  dataType: "json",

  // 成功获取后，执行这一步函数
  success: function(data) {
    // 将获取的数据装填
    initGeetest(
      {
        gt: data.gt,
        challenge: data.challenge,
        offline: !data.success,
        new_captcha: true,
        product: "float", // 显示模式为浮动
        width: "100%" // 显示宽度为父容器的 100%
      },
      function(captchaObj) {
        // 渲染验证码 GUI
        captchaObj.appendTo("#geetestGui");

        // 将数据装填到表单（会自动创建三个 input），进行二次校验
        captchaObj.bindForm("#mainForm");
      }
    );
  }
});
