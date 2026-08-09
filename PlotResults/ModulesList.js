myModules = [];

var FIRSTLOOP_data = [];
if (typeof myFIRSTLOOP != 'undefined' ) {
    FIRSTLOOP_data = JSON.parse(myFIRSTLOOP);
    myModules.push(FIRSTLOOP_data);
}

var PIT_data = [];
if (typeof myPIT != 'undefined' ) {
    PIT_data = JSON.parse(myPIT);
    myModules.push(PIT_data);
}

var GPRKO_data = [];
if (typeof myGPRKO != 'undefined' ) {
    GPRKO_data = JSON.parse(myGPRKO);
    myModules.push(GPRKO_data);
}

var PSK_data = [];
if (typeof myPSK != 'undefined' ) {
    PSK_data = JSON.parse(myPSK);
    myModules.push(PSK_data);
}

var PGBOX_data = [];
if (typeof myPGBOX != 'undefined' ) {
    PGBOX_data = JSON.parse(myPGBOX);
    myModules.push(PGBOX_data);
}

var SECLOOP_data = [];
if (typeof mySECLOOP != 'undefined' ) {
    SECLOOP_data = JSON.parse(mySECLOOP);
    myModules.push(SECLOOP_data);
}

var THIRDLOOP_data = [];
if (typeof myTHIRDLOOP != 'undefined' ) {
    THIRDLOOP_data = JSON.parse(myTHIRDLOOP);
    myModules.push(THIRDLOOP_data);
}

var SAOT_data = [];
if (typeof mySAOT != 'undefined' ) {
    SAOT_data = JSON.parse(mySAOT);
    myModules.push(SAOT_data);
}

var REACTORSIGNALS_data = [];
if (typeof myREACTORSIGNALS != 'undefined' ) {
    REACTORSIGNALS_data = JSON.parse(myREACTORSIGNALS);
    myModules.push(REACTORSIGNALS_data);
}

var COMMONFILES_data = [];
if (typeof myCOMMONFILES != 'undefined' ) {
    COMMONFILES_data = JSON.parse(myCOMMONFILES);
    myModules.push(COMMONFILES_data);
}

var COMBINED_data = [];
if (typeof myCOMBINED != 'undefined' ) {
    COMBINED_data = JSON.parse(myCOMBINED);
    myModules.push(COMBINED_data);
}

var AEROSOL_data = [];
if (typeof myAEROSOL != 'undefined' ) {
    AEROSOL_data = JSON.parse(myAEROSOL);
    myModules.push(AEROSOL_data);
}

