var componentMode;
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

function insertGrid(divSizes){
	var x=	$('<div class="ui container ab grid edit-area edit-area--div paint-area grid" style="margin:0"></div>');
	divSizes.forEach(function(yo){
		yo+=' edit-area paint-area';
		$('<div></div>').addClass(yo).append('<div class="paint-area paint-area--text edit-area edit-area--text" style=" ">hello-again-bc</div>').appendTo(x);
	});
	switch(componentMode){
		case 'after':
			$(x).insertAfter($('.selected-area'));
			break;
		case 'before':
			$(x).insertBefore($('.selected-area'));
			break;
		case 'into':
			$(x).appendTo($('.selected-area'));
			break;
		default:
			console.log('WTF! Chu hai kya be :|');
	}

}
function insertDiv(){
	var divSize=$('.divSizeSelector>.column').attr('class').replace('ui-resizable','');
	var x=$('<div></div>').addClass(divSize+' edit-area paint-area').append('<div class="paint-area paint-area--text edit-area edit-area--text" style=" ">hello-again-bc</div>');
	switch(componentMode){
		case 'after':
			$(x).insertAfter($('.selected-area'));
			break;
		case 'before':
			$(x).insertBefore($('.selected-area'));
			break;
		case 'into':
			$(x).appendTo($('.selected-area'));
			break;
		default:
			console.log('WTF! Chu hai kya be :|');
	}

}

$(document).ready(function(){


	function init(){
		//SET INSERT MODE
		componentMode=$('.insertModeButton.active').data('mode');
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

		//INTIALIZE DIV RESIZE - GRID
		resizer($('.sizeSelector>.column'));


		//INSERT GRID BUTTON
		$('.insert-grid').click(function(){
			var divSizes=getDivSizes();
			insertGrid(divSizes);
		});


		//DIV INSERT INIT
		$('.divSizeSelector>.column').resizable({handles:'e'}).bind({
			resizestart:function(event,ui){
				$(event.target).attr('class','column');
			},
			resizestop:function(event,ui){
				var widthOfOneDiv=$('.divColumnSetup>.column').outerWidth();
				var widthOfResizable=$(event.target).width();
				var x=Math.round(widthOfResizable/widthOfOneDiv);
				$(event.target).addClass(angreejiCounting[x]+' wide column').css('width','');
			}
		});

		//INSERT DIV BUTTON
		$('.insert-div').click(function(){
			insertDiv();
		});
	}
	init();
	$('.ui.accordion').accordion();
});