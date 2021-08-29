chrome.contextMenus.create({
	title: '使用 Trans 翻译：%s',
	contexts: ['selection'],
	onclick: function(params)
	{
		var xhr = new XMLHttpRequest();
		xhr.open("POST", "http://127.0.0.1:1024/t", true);
		xhr.onload = function (e) {
			alert(xhr.responseText);
		}
		xhr.onerror = function (e) {
			alert("划词范围过长，请缩短选中范围");
		}
        	xhr.send(params.selectionText);
	}
});