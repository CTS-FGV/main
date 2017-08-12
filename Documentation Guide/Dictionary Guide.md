<img src="https://pbs.twimg.com/profile_images/491026206062428160/UNCi6hwE.png" width="160" height="160" >

##Introduction
-------------

This a guide is about how your dictionary, about your data, should be create.

----------------
 
### What file format I have to use?

The main rule is to be saved as a csv or a json.

-----------
### Rules you have to follow

The dictionary need to have a key named as **"id"**,  and this key need to follow these rules:

> - Need to be a **unique** number per variable_name;
> - Need to appear **every line** you have a variable_name.

The dictionary need to have a key named as **"variable_name"**, and this key need to follow these rules:

> - Need to be **equal** to the variable_name of your database;
> - Contain all of your database variables.

The dictionary need to have a key named as **"variable_description"**, and this key need to follow these rules:

> - Has to be a string who contain the **best explanation** about your variable,
> - Need to appear **every line** you have a variable_name.

The dictionary need to have a key named as **"variable_type"**, and this key need to follow these rules:

>- Has to be a string who contain:
 - discrete, if your variable has only integer;
 - continuous, if your variable has  fractionals values;
 - categorical, If your variable has categoricals values;;
 - text, if your variable has texts;
 - datatime, if your variable has a data or time.
> - Need to appear **every line** you have a variable_name.

The dictionary need to have a key named as **"categorical_code"** , and this key need to follow these rules:

>- Must be empty if your variable is not categorical;
>- You need to create a new line for every category;
>- Need to contain the code or name of the category. 

The dictionary need to have a key named as **"categorical_description"**, and this key need to follow these rules:

>- Must be empty if is not categorical;
>- There must be one per categorical_code;
>- Need to contain the description of that category.


---------------------
### Example

If you read your dictionary as a data frame, should be something like that

| id | variable_name | variable_description | variable_type | categorical_code | categorical description   |
| :------- | ----: | :---: | :---: | :---: | :---: |
| 098f | count_of_bikes |  The number of bikes which are used at that time  | discrete | | |
| 097c | raining |  If at that time was raining or not  | categorycal | 0 | wasn't raining | 
| 097c | raining |  If at that time was raining or not  | categorycal | 1 | was raining | 
| 077h | income | Amount earned in an hour with bicycles  | continuos |  |  |
| 033h | comments | Comments about our bikes, randomly selected from all users, who used at that time. | text |  |  |
| 012a | data | Date and time the data was collected | datatime |  |  |