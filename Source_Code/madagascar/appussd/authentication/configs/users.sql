create table users ( 
    username varchar(20), 
    salt varchar(20), 
    password varchar(50), 
    attempts number(5), 
    created_at timestamp(6), 
    modified_at timestamp(6),
    CONSTRAINT "users_pk" PRIMARY KEY (username)
)
/
