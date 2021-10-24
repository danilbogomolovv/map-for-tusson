# Web application for tracking objects on the map
## Filling the database
The application allows you to carry out many operations with objects on the map. Initially, the database is filled from a prepared xml file with information about objects, including addresses of objects, which are subsequently geocoded into coordinates. If the coordinates of the object were geocoded incorrectly, the user can manually change its location.

![me](https://github.com/danilbogomolovv/map-for-tusson/blob/main/demo/filling_the_database.gif)

## Searching and filter
### Searching
On the main page, you can search for objects by 3 attributes or by zones where objects are located. When you search, a window will be displayed with additional information about the found objects

![me](https://github.com/danilbogomolovv/map-for-tusson/blob/main/demo/searching.gif)

### Filter

On the filter page, you can find the objects you need by any attribute. In the screenshot below, we found all objects with SPg7 terminals, "Белгазпромбанк" bank in the city of Minsk.

![me](https://github.com/danilbogomolovv/map-for-tusson/blob/main/demo/filter.jpg)

## Requests

You can also view requests for repairs and equipment installation. You can search for a specific object using a filter with almost all the attributes of an object, or by looking at all object identification numbers.

![me](https://github.com/danilbogomolovv/map-for-tusson/blob/main/demo/requests.gif)

## Routes

You can build routes between two addresses or between two Tusson bases. The route will be built taking into account the objects to which you need to call.

![me](https://github.com/danilbogomolovv/map-for-tusson/blob/main/demo/routes.gif)
