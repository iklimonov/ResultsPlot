myCalcParameters
if (typeof myCalcParameters != 'undefined') {
	CalcParametersData = JSON.parse(myCalcParameters);
} else {
	myCalcParameters = { reactor: "\"Лучший\"", fuelType: "\"хорошим\"", accident: "\"опасная\""};
}

var CORE_data = [];
var BERKUT_data = [];
var DN3D_data = [];
var SAFR_data = [];
var SAFR_CF_data = [];
var FIRSTLOOP_data = [];
var SECLOOP_data = [];
var THIRDLOOP_data = [];
var SAOT_data = [];
var COMBINED_data = [];
var REACTORSIGNALS_data = [];
var COMMONFILES_data = [];
var BERKUT_N_data = [];
var AEROSOL_data = [];


myModules = [];

if (typeof myCORE != 'undefined' ) {
	CORE_data = JSON.parse(myCORE);
	myModules.push(CORE_data);
}
if( typeof myBERKUT != 'undefined' ) {
	BERKUT_data = JSON.parse(myBERKUT);
	myModules.push(BERKUT_data);
}
if( typeof myDN3D != 'undefined' ) {
	DN3D_data = JSON.parse(myDN3D);
	myModules.push(DN3D_data);
}
if (typeof mySAFR != 'undefined') {
	SAFR_data = JSON.parse(mySAFR);
	myModules.push(SAFR_data);
}
if (typeof mySAFR_CF != 'undefined') {
	SAFR_CF_data = JSON.parse(mySAFR_CF);
	myModules.push(SAFR_CF_data);
}
if (typeof myFIRSTLOOP != 'undefined') {
	FIRSTLOOP_data = JSON.parse(myFIRSTLOOP);
	myModules.push(FIRSTLOOP_data);
}
if (typeof mySECLOOP != 'undefined') {
	SECLOOP_data = JSON.parse(mySECLOOP);
	myModules.push(SECLOOP_data);
}
if (typeof myTHIRDLOOP != 'undefined') {
	THIRDLOOP_data = JSON.parse(myTHIRDLOOP);
	myModules.push(THIRDLOOP_data);
}
if (typeof mySAOT != 'undefined') {
	SAOT_data = JSON.parse(mySAOT);
	myModules.push(SAOT_data);
}
if (typeof myCOMBINED != 'undefined') {
	COMBINED_data = JSON.parse(myCOMBINED);
	myModules.push(COMBINED_data);
}
if (typeof myREACTORSIGNALS != 'undefined') {
	REACTORSIGNALS_data = JSON.parse(myREACTORSIGNALS);
	myModules.push(REACTORSIGNALS_data);
}
if (typeof myCOMMONFILES != 'undefined') {
	COMMONFILES_data = JSON.parse(myCOMMONFILES);
	myModules.push(COMMONFILES_data);
}
if (typeof myBERKUT_N != 'undefined') {
	BERKUT_N_data = JSON.parse(myBERKUT_N);
	myModules.push(BERKUT_N_data);
}
if (typeof myAEROSOL != 'undefined') {
	AEROSOL_data = JSON.parse(myAEROSOL);
	myModules.push(AEROSOL_data);
}





