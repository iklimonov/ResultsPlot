var myCalcParameters = '{  "reactor": "БН 1200М", "fuelType": "MOX", "accident": "LOF_1151"}';
if (typeof myCalcParameters != 'undefined') {
    CalcParametersData = JSON.parse(myCalcParameters);
} else {
    myCalcParameters = { reactor: "Лучший", fuelType: "хорошим", accident: "опасная"};
}
