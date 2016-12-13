create or replace procedure update_users( p_name varchar, p_salt varchar, p_password varchar, p_attempts number )
as
begin 
    merge into users m using dual on ( username = p_name )
    when not matched then insert ( username, salt, password, attempts, modified_at ) values ( p_name, p_salt, p_password, p_attempts, systimestamp )
    when matched then update set modified_at = systimestamp , salt = p_salt , password = p_password , attempts = p_attempts ;
end update_users;
/
