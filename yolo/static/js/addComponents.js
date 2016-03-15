var componentMode="before";
function insertTemplate(templateId){
	templateId="'#"+templateId+"'";
	$(target).html($(templateId).html);
}
$(document).ready(function(){
	function init(){

		//SET INSERT MODE
		$('.insertModeButton').click(function(){
			$(this).addClass('active').siblings('.button').removeClass('active');
			componentMode=$(this).attr('data-mode');
		});
	}
	init();
	$('.ui.accordion').accordion();
});