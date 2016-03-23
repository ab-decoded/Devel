var componentMode="before";
function insertTemplate(templateId){
	templateId="'#"+templateId+"'";
	$(target).html($(templateId).html);
}

var angreejiCounting=['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen'];

function resizer(e){
	e.resizable({handles:'e'}).bind({
		resizestart:function(event,ui){
			$(event.target).attr('class','column');
		},
		resizestop:function(event,ui){
			var widthOfOneDiv=$('.columnSetup>.column').outerWidth();
			var widthOfResizable=$(event.target).width();
			var x=Math.round(widthOfResizable/widthOfOneDiv);
			$(event.target).addClass(angreejiCounting[x]+' wide column').css('width','');
		}
	});
}



function getDivSizes(){
	var divSizes=[];
	$('.sizeSelector>.column').each(function(){
		divSizes.push($(this).attr('class').replace('ui-resizable',''));
	});
	console.log(divSizes);
	return divSizes;
}

$(document).ready(function(){


	function init(){
		//SET INSERT MODE
		$('.insertModeButton').click(function(){
			$(this).addClass('active').siblings('.button').removeClass('active');
			componentMode=$(this).attr('data-mode');
		});

		//SET DIVS IN GRID
		$('#divsCount').change(function(){
			var count=$(this).val();
			var temp=count,x=0,opacity=0.2;
			$('.sizeSelector').html('');
			while(temp--)
			{
				x=16/count;
				x=Math.floor(x);
				var e=$('<div class="'+ angreejiCounting[x]+ ' wide column" style="opacity:'+opacity+'"></div>');
				resizer(e);
				$('.sizeSelector').append(e);
				opacity+=0.15;
			}
		});

		//INTIALIZE DIV RESIZE
		resizer($('.sizeSelector>.column'));

		//INSERT BUTTON
		$('.insert-grid').click(function(){
			var divSizes=getDivSizes();

		});
	}
	init();
	$('.ui.accordion').accordion();
});