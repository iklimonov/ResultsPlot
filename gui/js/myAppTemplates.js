
var myTemplateModule = '<h1 class="h3 text-center mt-5">Результаты расчёта полученные модулем {{myModule.name}}</h1>' +
	'<h2 class="lead text-center">Реактор {{myTask.reactor}}. Авария типа {{myTask.accident}} с типом топлива {{myTask.fuelType}}</h2> <hr class="mb-5">' +
	' <section> <h1></h1> <div ng-repeat="sb in myModule.subgroups"><hr class="mb-3"> <p style="font-weight: bold; font-size: 14pt;">{{sb.title}}</p>  <div ng-repeat="pic in sb.pictures" style="margin-bottom:20px"> <figure> <img ng-src="{{pic.url}}"> <figcaption class="text-center font-weight-bolder"><b>Рисунок {{$index+1}} - {{pic.discription}}</b></figcaption> </figure> </div> </div> </section> ';

var myTemplateMain = '<h1 class="h3 text-center mt-5">Результаты расчёта полученные кодом ЕВКЛИД/V2</h1>' +
	' <h1 class="h4 text-center mt-2">Реактор {{myTask.reactor}}. Авария типа {{myTask.accident}} с типом топлива {{myTask.fuelType}}</h1>' +
	' <hr class="mb-5">' +
	' <h2 class="lead text-center">Выберите группу данных для просмотра результатов</h2>' +
	'<div class="list-group">' +
	'  <a ng-repeat="myMod in allModules" href="#!{{myMod.name}}" class="list-group-item list-group-item-action list-group-item-success">{{myMod.title}}</a>' +
	'</div>';

var myTemplateSubGroup = '' +
	'<h1 class="h3 text-center mt-5">Результаты расчёта: {{subGroup.title}}</h1>' +
	'<h2 class="lead text-center">Реактор {{myTask.reactor}}. Авария типа {{myTask.accident}} с типом топлива {{myTask.fuelType}}</h2>' +
	'<hr class="mb-5">' +
	'<section>' +
	'    <h1></h1>' +
	'    <div >' +
	'        <hr class="mb-3">' +
	'        <div ng-repeat="pic in subGroup.pictures" style="margin-bottom:20px">' +
	'            <figure>' +
	'                <img ng-src="{{pic.url}}">' +
	'                <figcaption class="text-center"><b>Рисунок {{ $index+ 1}} - {{ pic.discription }}</b></figcaption>' +
	'            </figure>' +
	'        </div>' +
	'        <h1></h1>' +
	'    </div>' +
	'</section> ';

var myTemplateSubGroupSlider = '' +
	'<h1 class="h3 text-center mt-5">Результаты расчёта: {{subGroup.title}}</h1>' +
	'<h2 class="lead text-center">Реактор {{myTask.reactor}}. Авария типа {{myTask.accident}} с типом топлива {{myTask.fuelType}}</h2>' +
	'<hr class="mb-5">' +
	'<script >' +
	'    var slideIndex = 0;' +
	'</script>' +
	'<section>' +
	'	<h1></h1>' +
	'	<hr class="mb-3"> ' +
	'	<div class="w3-content w3-display-container" >' +
	'		<div class="w3-display-container mySlides" ng-repeat="pic in subGroup.pictures">' +
	'			<img ng-src="{{pic.url}}" alt = "{{pic.discription}}" >' +
	'			<div class="w3-display-bottom w3-large w3-container w3-padding-16 w3-black w3-round-xlarge">' +
	'				<b>Рисунок {{$index+1}} - {{pic.discription}}</b>' +
	'			</div>' +
	'		</div>' +
	'	</div>' +
	'		<div class="w3-center w3-container w3-section w3-large w3-text-white w3-display-bottom" >' +
	'			<button class="w3-button w3-display-left w3-red" onclick="plusDivs(-1)" style = "height: 20%; left:14px">&#10094;</button>' +
	'			<button class="w3-button w3-display-right w3-red" onclick="plusDivs(1)" style = "height: 20%; right:14px">&#10095;</button>' +
	'		</div>' +
	'</section>';
