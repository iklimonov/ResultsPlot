app.controller('mainCtrl', function ($scope, $location) {
	$scope.myTask= CalcParametersData
	$scope.allModules = [];
	$scope.allModules = myModules;
	//var current_url = $location.path()
	//var str_arr = current_url.split('/');
	//var modul = str_arr[1];
	//var subgroup = str_arr[2];
	//alert($location.path());
	slideIndex = 1;

});

app.controller('subgroupCtrl', function ($scope, $routeParams) {
	// меню
	$scope.myTask = CalcParametersData
	$scope.allModules = [];
	$scope.allModules = myModules;
	// 
	var my_module = $routeParams.idModule;
	var my_subgroup = $routeParams.idSubGroup;
	var sub_data = [];
	for (i = 0, len = myModules.length; i < len; i++) {
		if (myModules[i].name == my_module) {
			for (j = 0; j < myModules[i].subgroups.length; j++) {
				if (myModules[i].subgroups[j].name == my_subgroup) {
					sub_data = myModules[i].subgroups[j];
					break;
				}
			}
			break;
		}
	}
	$scope.subGroup = sub_data;
	slideIndex = 0;
});

app.controller('moduleCtrl', function ($scope, $routeParams) {
	// меню
	$scope.myTask = CalcParametersData
	$scope.allModules = [];
	$scope.allModules = myModules;
	// 
	var my_module = $routeParams.idModule;
	var mod_data = [];
	for (i = 0, len = myModules.length; i < len; i++) {
		if (myModules[i].name == my_module) {
			mod_data = myModules[i];
			break;
		}
	}
	$scope.myModule = mod_data;
});
