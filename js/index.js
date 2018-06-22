function run() {
    var text = document.getElementById('body').value,
        target = document.getElementById('MDOut'),
        converter = new showdown.Converter({
            tables: true,
            strikethrough: true
        }),
        html = converter.makeHtml(text);

    target.innerHTML = html;
    target.style.display = 'block';
}
