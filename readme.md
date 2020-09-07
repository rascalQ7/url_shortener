#### About:

##### Application has basic authentication
* Views are protected and available only for authorized users;
* Application redirects unauthorized user to login/, singup/ views;

##### Url shortener UI
* Authorized user can shorten url at the index page - /;
* Authorized user can view his own generated valid[1] urls at /dashboard/;
* Authorized user can deactivate generated url via /dashboad/;

#### Url shortener
* Shot url is generated by converting number to a higher base. Currently it is set to Base62 - [0-9], [a-z], [A-Z];
* Number for short url is record's ID. Currently number is set between 100000 - ZZZZZZ (BASE62) to have quite short url with around 31 milliard available combinations;
* Record's id is generated as pseudo random number by using LCG algorithm and previous records ID as a seed. Ref: [Wiki LCG](https://en.wikipedia.org/wiki/Linear_congruential_generator);

#### Url meta
* Every redirection is logged to DB with some additional meta data which is available only in admin panel;

#### Business config
* Config variables are stored in db table ConfigItem;
* Default configuration should be loaded from fixtures;
* Super user can modify thresholds of url expiration time and redirection limit via admin panel; 

##### DB relations
User 1 <-> M Tiny URL 1 <-> M Tiny URL's meta   

[1] Valid url complies with these rules:
* Url is not expired
* Url is not deactivated
* Url is not over redirection limit


#### Start application:

1. Generate database objects:

    `python manage.py makemigrations`

    `python manage.py migrate`
    
1. Generate config items from fixtures:
    
    `python manage.py loaddata tiny_urls/fixtures/config_items.json`

1. Create superuser:

    `python manage.py createsuperuser`

1. Start url shortener service locally:

    `pip install -r requirements.txt`
    
    `python manage.py runserver`

    Or as docker container:

    `docker-compose up`

1. Open home page: [localhost](http://localhost:8000)