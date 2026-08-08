app.config(function ($routeProvider) {
	$routeProvider
		.when("/:idModule/:idSubGroup", {
			template: myTemplateSubGroup,
			controller: "subgroupCtrl"//"dn3dCtrl"
		})
		.when("/:idModule/", {
			template: myTemplateModule,
			controller: "moduleCtrl"//"dn3dCtrl"
		})
		.when("", {
			template: myTemplateMain,
			controller: "mainCtrl"//"dn3dCtrl"
		})
		.otherwise({
			template: myTemplateMain,
			controller: "mainCtrl"
		});

});