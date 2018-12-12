/*Import dataset*/
PROC IMPORT OUT= WORK.city_correlation 
            DATAFILE= "\mids_capstone\vaxxfacts\cleaning_etl\city_correlation.csv" 
            DBMS=CSV REPLACE;
     GETNAMES=YES;
     DATAROW=2; 
RUN;

/*Create new variable to classify binary reaching herd immunity or not with 92 as the cut off*/
/*Less than 92 is not Herd Immunity*/
/*Greater than or equal to 92 is Herd Immunity*/
data regression;
	set city_correlation;
if vac_pct ge 92 then herd='Yes'; 
if vac_pct lt 92 then herd='No';
run;

ods pdf file='\mids_capstone\vaxxfacts\cleaning_etl\city_correlation.csv\RegressionOutput.pdf';
proc logistic data=regression;
title '2012';
class herd (ref='Yes')/param=ref;
model herd=tot_pop male_pct median_age   
	hispanic_latino_pct white_pct black_pct aian_pct asian_pct nhopi_pct other_pct 
	no_insurance_pct bachelor_degree_pct/lackfit;
where year=2012;
run;

proc logistic data=regression;
title '2013';
class herd (ref='Yes')/param=ref;
model herd=tot_pop male_pct median_age   
	hispanic_latino_pct white_pct black_pct aian_pct asian_pct nhopi_pct other_pct 
	no_insurance_pct bachelor_degree_pct/lackfit;
where year=2013;
run;

proc logistic data=regression;
title '2014';
class herd (ref='Yes')/param=ref;
model herd=tot_pop male_pct median_age   
	hispanic_latino_pct white_pct black_pct aian_pct asian_pct nhopi_pct other_pct 
	no_insurance_pct bachelor_degree_pct/lackfit;
where year=2014;
run;

proc logistic data=regression;
title '2015';
class herd (ref='Yes')/param=ref;
model herd=tot_pop male_pct median_age   
	hispanic_latino_pct white_pct black_pct aian_pct asian_pct nhopi_pct other_pct 
	no_insurance_pct bachelor_degree_pct/lackfit;
where year=2015;
run;

proc logistic data=regression;
title '2016';
class herd (ref='Yes')/param=ref;
model herd=tot_pop male_pct median_age   
	hispanic_latino_pct white_pct black_pct aian_pct asian_pct nhopi_pct other_pct 
	no_insurance_pct bachelor_degree_pct/lackfit;
where year=2016;
run;
ods pdf close;

/*2017 and 2018 were not included since demographic data is as of 2016 and 2016 was used as a proxy for 2017 and 2018*/

/*proc logistic data=regression;*/
/*title '2017';*/
/*class herd (ref='immune')/param=ref;*/
/*model herd=tot_pop male_pct median_age   */
/*hispanic_latino_pct white_pct black_pct aian_pct asian_pct nhopi_pct other_pct no_insurance_pct bachelor_degree_pct/lackfit;*/
/*where year=2017;*/
/*run;*/
/**/
/*proc logistic data=test;*/
/*title '2018';*/
/*class herd (ref='immune')/param=ref;*/
/*model herd=tot_pop male_pct median_age   */
/*hispanic_latino_pct white_pct black_pct aian_pct asian_pct nhopi_pct other_pct no_insurance_pct bachelor_degree_pct/lackfit;*/
/*where year=2018;*/
/*run;*/

