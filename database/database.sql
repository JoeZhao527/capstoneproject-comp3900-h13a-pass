create table Users {
    f_name  text,
    l_name  text,
    email   text,
    password    text,
    phone_number    integer,
    id  serial primary key
};

create table Diners {
   diner_id  serial primary key,
   foreign key (diner_id) references Users(id)
};

create table Eateries {
    eatery_id   serial primary key,
    name    text,
    address text,
    menu    text,
    description text,
    schedule_id integer,
    foreign key(eatery_id) references Users(id)
};

create table Images {
    image_id integer references Eateries(eatery_id),
    image   text,
    primary key(image_id, image)
};

create table Vouchers {
    voucher_id  serial,
    eatery_id   integer,
    discount    Discount,
    date    Date,
    time_range  Date,
    foreign key(eatery_id) references Eateries(eatery_id)
    primary key(eatery_id, voucher_id)
};

create table Schedules {
    schedule_id serial,
    eatery_id   integer,
    no_vouchers integer,
    weekday     Weekdays,
    discount    Discount,
    foreign key (eatery_id) references Eateries(eatery_id),
    primary key(schedule_id, eatery_id)
};

create table Reviews {
    review_id   serial,
    diner_id    integer references Diners(diner_id),
    eatery_id   integer references Eateries(eatery_id),
    comment     text,
    rating      Ratings,
    primary key (diner_id, eatery_id, review_id)
};

create table Offers {
    schedule_id    integer references Schedules(schedule_id),
    voucher_id  integer references Vouchers(voucher_id),
    primary key (diner_id, voucher_id)
}

create table Bookings {
    diner_id    integer references Diners(diner_id),
    voucher_id  integer references Vouchers(voucher_id),
    if_used     boolean,
    primary key (diner_id, voucher_id)
}

CREATE DOMAIN Weekdays AS 
   CHECK (VALUE IN ('Mon','Tues','Wed','Thurs','Fri', 'Sat', 'Sun'));
CREATE DOMAIN Ratings AS 
   CHECK (VALUE > 0 AND VALUE < 6);
CREATE DOMAIN Discount AS 
   CHECK (VALUE > 0 AND VALUE <= 100);

