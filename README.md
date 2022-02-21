# covid_vaccine_provinces

## Variables
Date </br> 
Province </br> 
Province_th </br>
region (NESDC region) </br>
population (MOPH calculation, see below) </br>
Cases (number of daily cases) </br>
cases14days	(14-day moving average of number of daily cases) </br>
case14percap (14-day moving average of number of daily cases divided by population)</br> 
cases_cum	(number of total cases) </br>
case_cum_percap	(number of total cases divided by population) </br>
Deaths	</br>
Tests	</br>
Vac Given 1 Cum new	(number of population who have received 1st vaccination) </br>
Vac Given 2 Cum new	(number of population who have received 2nd vaccination)</br>
Vac Given 3 Cum new	(number of population who have received 3rd vaccination)</br>
1vacpercap (number of population who have received 1st vaccination divided by population, %) </br>
2vacpercap (number of population who have received 2nd vaccination divided by population, %)</br>
3vacpercap (number of population who have received 3rd vaccination divided by population, %)</br>

## Data source:
### djay/covidthailand (https://github.com/djay/covidthailand) </br>
moph_dashboard_prov.csv (cases, deaths, tests; vac given 1, vac given 2, vac given 3 - since January 21, 2022) </br>
vaccinations.csv (vac given 1, vac given 2, vac given 3 - until Janunary 20, 2022) </br>

### Population 
Compiled by MOPH from registered population by province as of March 2021 (MOI Department of Administration) and latent population by province as of March 2021 (National Statistical Office). Data are obtained from MOPH's Report of COVID Vaccination Services of August 17th, 2021. </br>
https://ddc.moph.go.th/uploads/ckeditor2//files/Daily%20report%20%202021-08-17.pdf </br>

## Value edits
There are slight discrepancies found in numbers of total cases of official reports of different times. For example, total cases of day 1 plus new daily cases of day 2 does not equal to the officially reported total cases of day 2. Thus, we use official number of total cases by province of January 6, 2022 and perform backward & forward calculations from the baseline. Caused by backward calculation, 2 provinces have a very few days of minus total cases for the earliest days of first COVID cases in the province, namely Nakhon Panom and Sakon Nakhon. In those cases, the minus total cases are treated as 0. </br>
Missing or inconsistent values are interpolated on the following dates:
### 2021
April 14, 21, 30 </br>
May 1, 5 - 10, 14, 24 - 31 </br>
June 1 - 30 </br>
July 12 (Bangkok only, for anomal 1st and 2nd shot given), 26 - 27 </br>
August 30 - 31 </br>
September 1 - 3, 22 - 30 </br>
October 1 - 3 </br>
November 18, 29 - 30 (Mukdahan and Sing Buri only for anomal daily cases) </br>
December 12, 1 - 23 (Mukdahan and Sing Buri only for anomal daily cases), 24 - 27 (Mukdahan only for anomal daily cases) </br>
### 2022
January 4 - 6, 6 (Nan only for anomal daily cases) </br>

## Versions
January 6, 2022 </br>
February 23, 2022 </br>
February 22, 2022 </br>
