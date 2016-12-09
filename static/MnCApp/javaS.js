function myFunc(x){
	x.classList.toggle('change');
	document.getElementById('myDropdown').classList.toggle('show');
}
function openCity(evt, cityName){
	var i,tabcontent,tablinks;
	tabcontent=document.getElementsByClassName('tabcontent');
	for(i=0;i<tabcontent.length;i++){
		tabcontent[i].style.display='none';
	}
	tablinks=document.getElementsByClassName('tablinks');
	 for (i = 0; i < tablinks.length; i++) {
		 tablinks[i].className = tablinks[i].className.replace(" active", "");
	 }
	 document.getElementById(cityName).style.display = "block";
	 evt.currentTarget.className += " active";
}
function getCookie(name){
	if(document.cookie.length>0){
		start=document.cookie.indexOf(name+'=');
		if(start !=-1){
			start=start+name.length+1;
			end=document.cookie.indexOf(';'+start);
			if (end==-1) end=document.cookie.length;
			return unescape(document.cookie.substring(start,end));
		}
	}
	return "";
}
function display(obj){
	$.ajaxSetup({
		headers:{"X-CSRFToken":getCookie('csrftoken')}
	});
	$.post("/getMemo/",{memo_id:obj},function(data){
		$("#sub").text(data.subject);
		$("#sender").text("From: "+data.sender);
		$("#time").text(data.temporal_info);
		$("#body").text(data.body);
	});
	$('#myModal').css('display','block');
};