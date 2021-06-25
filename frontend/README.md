# data in frontend
### sprint 1: eatery related
- /eatery/register, POST  
```javascript
data = {
  fname: string,
  lname: string,
  email: string,
  password: string,
  ename: string,      // eatery name 
  cuisines: list,
  address: string,
  menu: file,          // not garantee to work
  description: string
}
```
- /login
```javascript
data = {
  email: string,
  password: string,
  utype: 'diner' or 'eatery'
}
```
- /logout
```javascript
data = {
  token: string
}
```
- /eatery/profile/edit
```javascript
data = {

}
```

- /eatery/profile/add_schedule
```javascript
data = {
  token: string // eatery token
  weekday: string // one of ['Monday', 'Tuesday' 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  type: string // one of ['breakfast', 'lunch', 'dinner']
  start: string // e.g. '00:00', '21:30', '7:20' etc. start time of the schedule
  end: string // e.g. '00:00', '21:30', '7:20' etc. end time of schedule
}
```
