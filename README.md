THE APPLICATION'S CURRENT DESIGN IS TAILORED EXCLUSIVELY FOR DESKTOP USAGE. MOBILE RESPONSIVENESS IS CURRENTLY UNDER DEVELOPMENT AND WILL BE IMPLEMENTED IN THE NEAR FUTURE.

SPACE CONTENT is a webapp using Nasa's API for retrieve images from space and Mars pictures took from the mars rover.
Users can choose between those 2 features to use the webapp. APOD(Astronomy Picture of the Day) and Mars Rover Pictures.
APOD can be filtered by date, start date and end date, count of images. "Date" filter needs to be used alone, can't be used combined with start date, end date and count. The same goes for "count" filter. 
It provides a picture for the specific date and an explanation about that image.
Mars Rover can be filtered by earth date and type of camera used by the mars rover. Users have to choose the earth date and then the type of camera chosen.

Users can also add those pictures to their favorites list, and delete it from there.



                                                                                                      --------- Technologies ---------

All back-end, server and routes are built using Python and Flask. 
Registration and Authentication using Bcrypt, so all the passwords are being saved on Database using hashed format. 
Forms created and handled using Flask WTForms.
Database created and managed using PostgreSQL and SQLAlchemy.
Front-end set with Javascript to handle interaction with add-to-favorite button.
Bootstrap and CSS to style pages.
