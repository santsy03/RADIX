''' core functions for the service '''
from utilities.logging.core import log
from utilities.secure.core import decrypt
from utilities.db.core import execute_query
from utilities.secure.core import salt as makesalt
from utilities.memcache.core import MemcacheHandler
from utilities.db.core import call_stored_procedure as make_user
from authentication.configs import (SQL, STATUS, service_name,
                                    DEFAULT_PASSWORD, ALLOWED_ATTEMPTS)
from configs.config import MEMCACHE_HOSTS

CACHE = MemcacheHandler(hosts=MEMCACHE_HOSTS)


def authenticate(resources, user, password):
    '''
    compare credentials received with stored credentials

    if auth fails, update attempts count on DB

    return status code
    '''
    try:
        cache_key = 'auth_user_%s' % str(user).strip()
        user_details = CACHE.get(cache_key)
        if user_details:
            log(resources, '%r - creds from cache: %r' % (user, user_details))
        else:
            args = {'username': user}
            execute_query(resources, SQL['authenticate'],
                    args, 'db_connection')
            user_details = resources['parameters']['cursor'].fetchall()
            resources['parameters']['cursor'].close()
            del(resources['parameters']['cursor'])
            log(resources, '%r-%r DB: salt, pwd - %r' % (
                user, password, user_details))
            if not user_details:
                # user does not exist
                log(resources, 'user %r does not exist' % user, 'info')
                return STATUS['no_user']
            else:
                CACHE.set(cache_key, user_details)
        attempts, salt, enc_password = \
                user_details[0][0], user_details[0][1], user_details[0][2]
        salted_password = decrypt(enc_password)
        unsalted_password = salted_password.replace(salt, '', 1)

        try:
            assert int(attempts) <= ALLOWED_ATTEMPTS
        except AssertionError:
            # exhausted attempts. Lock account
            log(resources, '%r -attempts exhausted account locked' % user)
            return STATUS['account_locked']

        try:
            assert password.strip() == unsalted_password.strip()
            log(resources, 'auth positive %s-%s' % (user, password))
            return STATUS['auth_success']
        except AssertionError:
            log(resources, 'auth fail %s-%s' % (user, password))

            # update attempts count:
            #on cache
            updated_user = [(int(attempts) + 1, salt, enc_password)]
            CACHE.set(cache_key, updated_user)

            # on DB:
            args = {'attempts': int(attempts) + 1,
                    'username': user}
            execute_query(resources, SQL['update_attempts'],
                    args, 'db_connection')
            resources['parameters']['cursor'].connection.commit()
            resources['parameters']['cursor'].close()
            del(resources['parameters']['cursor'])
            return STATUS['auth_fail']

    except Exception, err:
        auth_err = '%r - auth fail for %r - %r' % (service_name, user, err)
        log(resources, auth_err, 'error')
        return STATUS['error']


def create_user_account(resources, user, password=DEFAULT_PASSWORD):
    '''
    creates new user with password supplied
    default password is assigned if none is supplied
    '''
    try:
        resp = makesalt(password)
        salt, enc_password = resp[0], resp[1]
        log(resources, '%s - %s - %s' % (user, salt, enc_password))
        make_user(resources, SQL['procedure'],
                [user.strip(), salt, enc_password, 0], 'db_connection')
    except Exception, err:
        create_err = '%r.create_user_account() failed - %r - %r' % (
                service_name, user, err)
        log(resources, create_err, 'error')
        return STATUS['user_create_fail']
    else:
        log(resources, 'user %r created with %r' % (user, password))
        return STATUS['user_created']


def change_password(resources, user, old_password, new_password):
    '''
    performs authentication using old_password
    if authentication passes: overwrite user entry with new_password
    return status code
    '''
    try:
        auth = authenticate(resources, user, old_password)
        if auth == STATUS['auth_success']:
            created = create_user_account(resources, user, new_password)
            if created == STATUS['user_created']:
                # reset cache
                cache_key = 'auth_user_%s' % str(user).strip()
                CACHE.delete(cache_key)

                return STATUS['password_change_success']
            else:
                return STATUS['password_change_fail']['create_user_fail']
        else:
            # auth failure
            auth_fail = 'cannot change password for %s - auth failed' % user
            log(resources, auth_fail, 'debug')
            return STATUS['password_change_fail']['auth_fail']

    except Exception, err:
        change_err = '%r - change_password() fail - %r' % (user, err)
        log(resources, change_err, 'error')
        raise err


def unlock_account(resources, user):
    '''
    reset attempts to 0
    '''
    try:
        cache_key = 'auth_user_%s' % str(user).strip()
        args = {'attempts': 0,
                'username': user}
        execute_query(resources, SQL['unlock'], args,
                'db_connection')
        resources['parameters']['cursor'].connection.commit()
        resources['parameters']['cursor'].close()
        del(resources['parameters']['cursor'])
        CACHE.delete(cache_key)
        log(resources, 'Account %r unlocked' % user, 'info')
        return STATUS['unlock_success']
    except Exception, err:
        log(resources, '%r - unlock failed - %r' % (user, err), 'error')
        return STATUS['unlock_fail']


def reset_password(resources, user):
    '''
    reset attempts to 0
    reset password to default
    return status code
    '''
    try:
        cache_key = 'auth_user_%s' % str(user).strip()
        new_salt, new_password = makesalt(DEFAULT_PASSWORD)
        args = {'attempts': 0,
                'default_password': new_password,
                'salt': new_salt,
                'username': user}
        execute_query(resources, SQL['reset_password'],
                args, 'db_connection')
        resources['parameters']['cursor'].connection.commit()
        resources['parameters']['cursor'].close()
        del(resources['parameters']['cursor'])
        CACHE.delete(cache_key)
        log(resources, 'Password reset to default for %r' % user, 'info')
        return STATUS['password_reset_success']
    except Exception, err:
        log(resources, '%r - password reset fail - %r' % (user, err), 'error')
        return STATUS['password_reset_fail']
